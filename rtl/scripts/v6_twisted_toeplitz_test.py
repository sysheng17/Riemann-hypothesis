"""Twisted Toeplitz kernel positivity test for Riemann Hypothesis.

Tests whether the non-commutative deformation θ ≠ 0 can produce a positivity
condition different from the standard D̂(λ) ≥ 0 (which is equivalent to RH).

Kernel in Fourier domain: K_θ(μ,ν) = Re[e^{i(ν-μ)²/(4θ)} · D̂(-(ν+μ)/2)]

where D̂(λ) = Σ_p log p·p^{-iλ} + archimedean contribution.

References: rtl/theory/twisted_crossed_product_GNS.md
             rtl/theory/twisted_core_computation.md
"""

import numpy as np
from numpy.fft import fft, ifft, fftfreq
from scipy.special import digamma
from scipy.linalg import eigh, eigvalsh
import matplotlib.pyplot as plt
import warnings
import os

# === Constants ===
PRIME_CUTOFF = 200      # max prime for the sum
PRIMES = None           # will be computed
GAMMA_EULER = 0.57721566490153286060651209008240243104215933593992
LOG_2PI = np.log(2 * np.pi)

# === Prime utilities ===

def sieve_primes(limit):
    """Simple Sieve of Eratosthenes"""
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i*i:limit+1:i] = False
    return np.where(sieve)[0]

def get_primes(cutoff=PRIME_CUTOFF):
    global PRIMES
    if PRIMES is None:
        PRIMES = sieve_primes(cutoff)
    return PRIMES

# === Archimedean contribution ===

def xi_prime_over_xi(s):
    """Compute ξ'/ξ(s) = 1/s + 1/(s-1) - 0.5*log π + 0.5*Γ'/Γ(s/2) + ζ'/ζ(s)
    
    Returns the full ξ'/ξ(s) for given complex s.
    We'll compute the ζ'/ζ part from the prime sum (truncated).
    """
    primes = get_primes()
    # 1/s + 1/(s-1)
    term1 = 1.0 / s + 1.0 / (s - 1.0)
    # -0.5*log π
    term2 = -0.5 * np.log(np.pi)
    # 0.5*Γ'/Γ(s/2) 
    term3 = 0.5 * digamma(s / 2.0)
    # ζ'/ζ(s) ≈ -Σ_p log p·p^{-s} (ignoring higher prime powers)
    zeta_prime_over_zeta = -np.sum(primes * primes**(-s))
    return term1 + term2 + term3 + zeta_prime_over_zeta

def D_hat_archimedean(lmbda):
    """Archimedean contribution to D̂(λ).
    
    Uses the digamma function for the Gamma factor part.
    D̂_arch(λ) = -Re[ξ'/ξ(1/2 + iλ)]_arch (the non-prime part)
    """
    s = 0.5 + 1j * lmbda
    # Archimedean part of ξ'/ξ (excluding ζ'/ζ prime contribution)
    arch = 1.0 / s + 1.0 / (s - 1.0) - 0.5 * np.log(np.pi) + 0.5 * digamma(s / 2.0)
    # Add the conjugate for the full real part
    # We need: -Re[arch + zeta_prime_part]
    # The full D̂(λ) = -Re[ξ'/ξ(1/2+iλ)]
    # Split: D̂(λ) = -Re[arch] - Re[zeta_prime_part]
    # zeta_prime_part ≈ -Σ log p·p^{-s}
    # So -Re[zeta_prime_part] = Re[Σ log p·p^{-s}] = Σ log p·p^{-1/2}·cos(λ·log p)
    
    # For the archimedean part alone (to use in constructing D̂):
    # The prime part is Σ log p·p^{-iλ}, which is different from Re[Σ log p·p^{-s}]
    # 
    # Actually, let's use the known relation from the explicit formula.
    # D̂(λ) = Σ_p log p·p^{-iλ} + hatch(λ)
    # where hatch(λ) is the archimedean contribution.
    
    # From the explicit formula: D(t) = 1 + e^t - Σ_ρ e^{tρ}
    # = Σ_p log p·δ(t-log p) + hatch(t)
    # 
    # The Fourier transform: D̂(λ) = Σ log p·p^{-iλ} + ĥ(λ)
    # 
    # Using the ξ-function:
    # -ξ'/ξ(1/2 + iλ) = Σ_ρ 1/(1/2 + iλ - ρ)
    # Re[-ξ'/ξ(1/2 + iλ)] = Σ_ρ (1/2 - Re(ρ)) / ((λ-Im(ρ))² + (1/2-Re(ρ))²)
    # 
    # But ξ'/ξ = arch + ζ'/ζ where ζ'/ζ has the prime sum.
    # So: -Re[ξ'/ξ(1/2+iλ)] = -Re[arch(1/2+iλ)] - Re[ζ'/ζ(1/2+iλ)]
    # 
    # And the prime-part of D̂ is NOT the same as -Re[ζ'/ζ]. 
    # ζ'/ζ(s) = -Σ log p·p^{-s} - Σ log p·p^{-2s} - ... (all prime powers)
    # D̂(λ) prime part = Σ log p·p^{-iλ} (only k=1, no p^{-1/2} factor)
    #
    # The relationship:
    # -Re[ζ'/ζ(1/2+iλ)] = Σ log p·p^{-1/2}·cos(λ·log p) + higher powers
    # 
    # This is DIFFERENT from Re[Σ log p·p^{-iλ}] = Σ log p·cos(λ·log p)
    #
    # The difference is the p^{-1/2} factor, which comes from the functional equation.
    #
    # For the archimedean part:
    # D̂_arch(λ) = ĥ(λ) where D̂(λ) = Σ log p·p^{-iλ} + ĥ(λ)
    # 
    # We can compute ĥ(λ) by noting that:
    # D(t) = 1 + e^t - Σ_ρ e^{tρ}
    # And for t > 0, t ≠ log p:
    # D(t) = hatch(t) = (some smooth function)
    #
    # The Fourier transform ĥ(λ) = ∫ hatch(t)·e^{-iλt} dt
    return arch

def D_hat_arch_component(lmbda):
    """Compute the archimedean component of D̂(λ) explicitly.
    
    From the explicit formula, D̂(λ) = Σ_p log p·p^{-iλ} + ĝ(λ)
    
    The known closed form of D̂(λ) is:
    D̂(λ) = -Re[ξ'/ξ(1/2 + iλ)]
    
    where ξ(s) = s(s-1)π^{-s/2}Γ(s/2)ζ(s)
    
    So ĝ(λ) = D̂(λ) - Σ_p log p·p^{-iλ}
            = -Re[ξ'/ξ(1/2+iλ)] - Σ_p log p·p^{-iλ}
    """
    s = 0.5 + 1j * lmbda
    primes = get_primes()
    
    # ξ'/ξ(1/2+iλ) without the ζ part
    # = 1/s + 1/(s-1) - 0.5*log π + 0.5*Γ'/Γ(s/2)
    arch = 1.0/s + 1.0/(s-1.0) - 0.5*np.log(np.pi) + 0.5*digamma(s/2.0)
    
    # ζ'/ζ(s) ≈ -Σ log p·p^{-s} (truncated, ignoring higher prime powers)
    zeta_contrib = np.sum(primes * primes**(-s))
    
    # Full -Re[ξ'/ξ(1/2+iλ)]
    full_D_hat = -np.real(arch + zeta_contrib)
    
    # Prime part: Σ log p·p^{-iλ}
    prime_part = np.real(np.sum(primes * primes**(-1j * lmbda)))
    
    # The archimedean component fills the gap
    g_hat = full_D_hat - prime_part
    
    return g_hat

def compute_D_hat(lmbda):
    """Compute D̂(λ) = Σ_p log p·p^{-iλ} + ĝ(λ) using the full explicit formula.
    
    Uses the relation D̂(λ) = -Re[ξ'/ξ(1/2 + iλ)] - δ_correction
    where δ_correction accounts for higher prime powers and regularization.
    """
    s = 0.5 + 1j * lmbda
    primes = get_primes()
    
    # ξ'/ξ(s) = 1/s + 1/(s-1) - 0.5*log π + 0.5*Γ'/Γ(s/2) + ζ'/ζ(s)
    # ζ'/ζ(s) = -Σ_p log p·p^{-s} - Σ_p Σ_{k≥2} log p·p^{-ks}
    
    # Compute -Re[ξ'/ξ] (this gives D̂ up to a constant)
    # Actually, -Re[ξ'/ξ(1/2+iλ)] = Σ_ρ (Re(ρ)-1/2)/((λ-Im(ρ))²+(Re(ρ)-1/2)²)
    # which is ≥ 0 iff all zeros have Re(ρ) = 1/2
    
    arch = 1.0/s + 1.0/(s-1.0) - 0.5*np.log(np.pi) + 0.5*digamma(s/2.0)
    
    # ζ'/ζ with only prime powers (k=1)
    # For Re(s) > 1: ζ'/ζ(s) = -Σ_p log p/(p^s - 1)
    # For analytic continuation, we use the Dirichlet series with truncation
    zeta_prime = -np.sum(primes * primes**(-s))
    
    full_xixi = -np.real(arch + zeta_prime)
    return full_xixi

# === Kernel construction ===

def kernel_theta(mu, nu, theta, D_hat_func=None):
    """Compute the Hermitian kernel K_θ(μ,ν).
    
    K_θ(μ,ν) = Re[e^{i(ν-μ)²/(4θ)} · D̂(-(ν+μ)/2)]
    
    where D̂(λ) is the full Fourier transform of D(t).
    For θ = 0, limit gives K_0(μ,ν) ∝ δ(μ-ν)·D̂(μ).
    """
    if D_hat_func is None:
        D_hat_func = compute_D_hat
    
    if abs(theta) < 1e-15:
        # θ = 0 limit: diagonal kernel
        # K_0(μ,ν) = C · δ(μ-ν) · D̂(μ)
        # C chosen so the trace matches the continuum
        if abs(mu - nu) < 1e-10:
            alpha = -(mu + nu) / 2.0
            d_hat_val = D_hat_func(alpha)
            return d_hat_val
        else:
            return 0.0
    
    phase = np.exp(1j * (nu - mu)**2 / (4 * theta))
    alpha = -(nu + mu) / 2.0
    d_hat_val = D_hat_func(alpha)
    
    return np.real(phase * d_hat_val)

def construct_kernel_matrix(mu_grid, theta, D_hat_func=None):
    """Construct the discretized kernel matrix K_θ on a given μ-grid."""
    n = len(mu_grid)
    K = np.zeros((n, n), dtype=complex)
    
    for i in range(n):
        for j in range(n):
            K[i, j] = kernel_theta(mu_grid[i], mu_grid[j], theta, D_hat_func)
    
    # Ensure Hermiticity (numerical safety)
    K = (K + K.conj().T) / 2.0
    return K

def construct_kernel_matrix_fast(mu_grid, theta, D_hat_func=None):
    """Vectorized construction of kernel matrix."""
    if D_hat_func is None:
        D_hat_func = compute_D_hat
    n = len(mu_grid)
    MU, NU = np.meshgrid(mu_grid, mu_grid, indexing='ij')
    
    if abs(theta) < 1e-15:
        # θ = 0 limit: diagonal kernel
        d_hat_vals = np.array([D_hat_func(m) for m in mu_grid])
        K = np.diag(d_hat_vals)
        return K
    
    phase = np.exp(1j * (NU - MU)**2 / (4 * theta))
    alpha = -(NU + MU) / 2.0
    
    # Compute D_hat for all alpha values
    d_hat_vals = np.array([D_hat_func(a) for a in alpha.ravel()]).reshape(alpha.shape)
    
    K = np.real(phase * d_hat_vals)
    K = (K + K.T) / 2.0  # ensure symmetry
    return K

# === Direct t-space approach (alternative) ===

def T_f_gaussian(sigma, c, theta, num_primes=100):
    """Compute T_f(θ) for Gaussian test function f(t) = exp(-sigma*(t-c)^2).
    
    Uses the prime δ-contributions with analytical Gaussian integrals.
    T_f(θ) = Σ_p log p · I_p(sigma, c, θ) + archimedean term
    
    where I_p = ∫ exp(-sigma*(t-c)² - sigma*(t+log p-c)² - iθ*t*(t+log p)) dt
    """
    primes = get_primes()[:num_primes]
    
    total = 0.0
    
    for p in primes:
        log_p = np.log(p)
        # Coefficient: A = 2σ + iθ
        A = 2.0 * sigma + 1j * theta
        # Coefficient: B = 2σ(2c - log p) - iθ·log p
        B = 2.0 * sigma * (2.0 * c - log_p) - 1j * theta * log_p
        # Constant term: C = -σ[c² + (c-log_p)²]
        C = -sigma * (c**2 + (c - log_p)**2)
        
        # Gaussian integral: ∫ exp(-At² + Bt) dt = √(π/A)·exp(B²/(4A))
        integral = np.sqrt(np.pi / A) * np.exp(C + B**2 / (4.0 * A))
        
        total += log_p * np.real(integral)  # T_f must be real
    
    return total

def scan_theta_gaussian(sigma_values, c_values, theta_values, num_primes=50):
    """Scan θ values for multiple Gaussian test functions."""
    results = np.zeros((len(sigma_values), len(c_values), len(theta_values)))
    
    for i, sigma in enumerate(sigma_values):
        for j, c in enumerate(c_values):
            for k, theta in enumerate(theta_values):
                val = T_f_gaussian(sigma, c, theta, num_primes)
                results[i, j, k] = val
    
    return results

# === Fourier domain approach ===

def compute_spectral_kernel(theta, mu_range=(-20, 20), n_points=64, prime_cutoff=200):
    """Compute the kernel matrix in Fourier domain and its eigenvalues.
    
    Discretizes the kernel K_θ(μ,ν) = Re[e^{i(ν-μ)²/(4θ)} · D̂(-(ν+μ)/2)]
    """
    mu_grid = np.linspace(mu_range[0], mu_range[1], n_points)
    K = construct_kernel_matrix(mu_grid, theta)
    
    # Account for quadrature weights (trapezoidal rule)
    dmu = (mu_range[1] - mu_range[0]) / (n_points - 1)
    sqrt_w = np.full(n_points, np.sqrt(dmu))
    K_weighted = K * sqrt_w * sqrt_w[:, np.newaxis]
    
    eigenvalues = eigvalsh(K_weighted)
    return eigenvalues, K_weighted, mu_grid

# === Density of zeros via D̂ ===

def D_hat_density(lmbda, num_primes=500):
    """Compute D̂(λ) which, if ≥ 0, is the spectral density of zeros.
    
    For RH: D̂(λ) ≥ 0 ⇔ zeros at Re(ρ) = 1/2.
    D̂(λ) = -Re[ξ'/ξ(1/2 + iλ)]
    """
    return compute_D_hat(lmbda)

# === Main visualization ===

def plot_D_hat():
    """Plot D̂(λ) to see the baseline (should be ≥ 0 iff RH)."""
    lmbdas = np.linspace(-10, 10, 500)
    D_vals = np.array([compute_D_hat(l) for l in lmbdas])
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    ax1, ax2 = axes
    
    ax1.plot(lmbdas, D_vals)
    ax1.axhline(0, color='k', ls='--', alpha=0.3)
    ax1.set_xlabel('λ')
    ax1.set_ylabel('D_hat(lambda)')
    ax1.set_title('D_hat(lambda) = spectral density (>=0 iff RH)')
    ax1.grid(alpha=0.3)
    
    ax2.plot(lmbdas, np.maximum(D_vals, 0), 'g-', lw=2, alpha=0.7, label='Positive part')
    ax2.plot(lmbdas, np.minimum(D_vals, 0), 'r-', lw=2, alpha=0.7, label='Negative part')
    ax2.axhline(0, color='k', ls='--', alpha=0.3)
    ax2.set_xlabel('λ')
    ax2.set_ylabel('D_hat(lambda)')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_kernel(theta, mu_range=(-5, 5), n=64):
    """Plot the kernel matrix for given θ."""
    mu = np.linspace(mu_range[0], mu_range[1], n)
    K = construct_kernel_matrix_fast(mu, theta)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    im1 = axes[0].imshow(np.real(K), aspect='auto', cmap='RdBu', 
                          extent=[mu_range[0], mu_range[1], mu_range[1], mu_range[0]])
    axes[0].set_title(f'Re[K_theta], theta={theta:.3f}')
    plt.colorbar(im1, ax=axes[0])
    
    im2 = axes[1].imshow(np.imag(K), aspect='auto', cmap='RdBu',
                          extent=[mu_range[0], mu_range[1], mu_range[1], mu_range[0]])
    axes[1].set_title(f'Im[K_theta], theta={theta:.3f}')
    plt.colorbar(im2, ax=axes[1])
    
    evals = eigvalsh(K)
    axes[2].plot(evals, 'o-', ms=3)
    axes[2].axhline(0, color='k', ls='--', alpha=0.3)
    axes[2].set_title(f'Eigenvalues, min={evals[0]:.4f}')
    axes[2].set_xlabel('Index')
    axes[2].set_ylabel('Eigenvalue')
    axes[2].grid(alpha=0.3)
    
    plt.tight_layout()
    return fig

def scan_theta_spectral(theta_values, mu_range=(-10, 10), n_points=48, prime_cutoff=200):
    """Scan θ and record min eigenvalue of the kernel matrix."""
    # Update prime cutoff
    global PRIMES
    PRIMES = sieve_primes(prime_cutoff)
    
    min_evals = []
    full_spectra = []
    
    mu_grid = np.linspace(mu_range[0], mu_range[1], n_points)
    
    for theta in theta_values:
        K = construct_kernel_matrix_fast(mu_grid, theta)
        dmu = (mu_range[1] - mu_range[0]) / (n_points - 1)
        sqrt_w = np.full(n_points, np.sqrt(dmu))
        K_weighted = K * sqrt_w * sqrt_w[:, np.newaxis]
        evals = eigvalsh(K_weighted)
        min_evals.append(evals[0])
        full_spectra.append(evals)
        print(f"  theta={theta:.4f}: min_eig={evals[0]:.6f}, neg_count={np.sum(evals<0)}/{n_points}")
    
    return np.array(min_evals), np.array(full_spectra)

def plot_theta_scan(theta_values, min_evals, full_spectra=None):
    """Plot min eigenvalue vs θ."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    axes[0].plot(theta_values, min_evals, 'o-')
    axes[0].axhline(0, color='k', ls='--', alpha=0.3)
    axes[0].set_xlabel('θ (deformation parameter)')
    axes[0].set_ylabel('Minimum eigenvalue')
    axes[0].set_title('K_theta kernel: min eigenvalue vs theta')
    axes[0].grid(alpha=0.3)
    
    if full_spectra is not None:
        # Color map of spectrum
        im = axes[1].imshow(full_spectra.T, aspect='auto', cmap='RdBu',
                           extent=[theta_values[0], theta_values[-1], 
                                   0, full_spectra.shape[1]],
                           vmin=-np.abs(full_spectra).max(), vmax=np.abs(full_spectra).max())
        axes[1].set_xlabel('θ')
        axes[1].set_ylabel('Eigenvalue index')
        axes[1].set_title('Full spectrum vs theta')
        plt.colorbar(im, ax=axes[1])
    
    plt.tight_layout()
    return fig

# === Main execution ===

if __name__ == '__main__':
    import sys
    
    # Output directory
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'figures', 'twisted_toeplitz')
    os.makedirs(out_dir, exist_ok=True)
    
    print("=" * 60)
    print("TWISTED TOEPLITZ KERNEL ANALYSIS")
    print("Testing if theta != 0 changes the RH positivity condition")
    print("=" * 60)
    
    # === Step 1: Plot the baseline D̂(λ) ===
    print("\n[Step 1] Computing D_hat(lambda) baseline...")
    fig = plot_D_hat()
    fig.savefig(os.path.join(out_dir, 'D_hat_baseline.png'), dpi=100)
    plt.close(fig)
    print("  Saved D_hat_baseline.png")
    
    # === Step 2: Test Gaussian approach ===
    print("\n[Step 2] Testing Gaussian test functions...")
    sigma_vals = [0.1, 0.5, 1.0]
    c_vals = [0.0, 1.0, 2.0, 5.0]
    theta_vals = np.linspace(-2, 2, 41)
    
    results = scan_theta_gaussian(sigma_vals, c_vals, theta_vals, num_primes=50)
    
    # Find min and max
    min_val = results.min()
    max_val = results.max()
    print(f"  T_f(theta) range: [{min_val:.4f}, {max_val:.4f}]")
    print(f"  All non-negative: {min_val >= 0}")
    
    # Plot some slices
    fig, axes = plt.subplots(len(sigma_vals), len(c_vals), figsize=(15, 8))
    for i, sigma in enumerate(sigma_vals):
        for j, c in enumerate(c_vals):
            ax = axes[i, j] if len(sigma_vals) > 1 and len(c_vals) > 1 else axes
            if len(sigma_vals) == 1:
                ax = axes[j]
            elif len(c_vals) == 1:
                ax = axes[i]
            ax.plot(theta_vals, results[i, j, :])
            ax.axhline(0, color='k', ls='--', alpha=0.3)
            ax.set_title(f'σ={sigma}, c={c}')
            ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, 'gaussian_scan.png'), dpi=100)
    plt.close(fig)
    print("  Saved gaussian_scan.png")
    
    # === Step 3: Fourier domain kernel ===
    print("\n[Step 3] Constructing Fourier domain kernel K_theta...")
    
    # Single θ plot
    for theta in [0.1, 0.5, 1.0, 2.0, 5.0]:
        try:
            fig = plot_kernel(theta, mu_range=(-5, 5), n=48)
            fig.savefig(os.path.join(out_dir, f'kernel_theta_{theta:.2f}.png'), dpi=100)
            plt.close(fig)
            print(f"  Saved kernel_theta_{theta:.2f}.png")
        except Exception as e:
            print(f"  Error for θ={theta}: {e}")
    
    # === Step 4: Scan θ ===
    print("\n    [Step 4] Scanning theta values for kernel positivity...")
    
    # Fine scan near 0
    theta_fine = np.linspace(-1, 1, 41)
    print(f"  Fine scan: theta in [-1, 1], {len(theta_fine)} points")
    min_evals_fine, spectra_fine = scan_theta_spectral(
        theta_fine, mu_range=(-8, 8), n_points=40, prime_cutoff=100
    )
    fig = plot_theta_scan(theta_fine, min_evals_fine, spectra_fine)
    fig.savefig(os.path.join(out_dir, 'theta_scan_fine.png'), dpi=100)
    plt.close(fig)
    print("  Saved theta_scan_fine.png")
    
    # Wide scan
    theta_wide = np.linspace(-10, 10, 41)
    print(f"\n  Wide scan: theta in [-10, 10], {len(theta_wide)} points")
    min_evals_wide, spectra_wide = scan_theta_spectral(
        theta_wide, mu_range=(-8, 8), n_points=40, prime_cutoff=100
    )
    fig = plot_theta_scan(theta_wide, min_evals_wide, spectra_wide)
    fig.savefig(os.path.join(out_dir, 'theta_scan_wide.png'), dpi=100)
    plt.close(fig)
    print("  Saved theta_scan_wide.png")
    
    # === Summary ===
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Gaussian test: T_f(θ) min = {min_val:.6f}, max = {max_val:.6f}")
    print(f"  All non-negative: {min_val >= 0}")
    
    # Find θ values that maximize min eigenvalue
    best_idx = np.argmax(min_evals_fine)
    best_theta = theta_fine[best_idx]
    print(f"\n  Best θ (max min eigenvalue): {best_theta:.4f}")
    print(f"  Corresponding min eigenvalue: {min_evals_fine[best_idx]:.6f}")
    
    worst_idx = np.argmin(min_evals_fine)
    worst_theta = theta_fine[worst_idx]
    print(f"  Worst θ (min min eigenvalue): {worst_theta:.4f}")
    print(f"  Corresponding min eigenvalue: {min_evals_fine[worst_idx]:.6f}")
    
    print(f"\n  Kernel positive definite for some θ: {np.any(min_evals_fine > 1e-10)}")
    print(f"  Kernel positive semi-definite for some θ: {np.any(min_evals_fine > -1e-10)}")
    
    print("\nDone!")
