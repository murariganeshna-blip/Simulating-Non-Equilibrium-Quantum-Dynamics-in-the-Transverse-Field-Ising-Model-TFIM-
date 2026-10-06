import os
import sys

# 1. Install required libraries
print("Installing required quantum libraries... This might take 30-60 seconds...")
os.system(f"{sys.executable} -m pip install -q qiskit qiskit-aer numpy scipy")
print("Installation complete! Running the quantum simulation...\n")

# 2. Imports
import numpy as np
from scipy.linalg import expm
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter
from qiskit.primitives import StatevectorEstimator

# 3. System parameters
num_spins = 4
J = 1.0
h = 1.0
time = 1.5

# 4. TFIM Hamiltonian: H = -J * sum(Z_i Z_{i+1}) - h * sum(X_i)
zz_interactions = [("ZZ", [i, i + 1], -J) for i in range(num_spins - 1)]
x_fields = [("X", [i], -h) for i in range(num_spins)]
hamiltonian = SparsePauliOp.from_sparse_list(zz_interactions + x_fields, num_qubits=num_spins)

# 5. Observable: average magnetization Mz = (1/N) * sum(Z_i)
z_obs = [("Z", [i], 1.0 / num_spins) for i in range(num_spins)]
magnetization_op = SparsePauliOp.from_sparse_list(z_obs, num_qubits=num_spins)

# 6. Exact reference (feasible for small N): |psi(t)> = exp(-iHt)|0000>
psi0 = Statevector.from_label("0" * num_spins).data
psi_t = expm(-1j * time * hamiltonian.to_matrix()) @ psi0
exact = float(np.real(psi_t.conj() @ magnetization_op.to_matrix() @ psi_t))

# 7. Sweep Trotter steps
estimator = StatevectorEstimator()
trotter_steps_range = [1, 2, 4, 6, 8, 10, 15, 20, 40]

print("=" * 72)
print("  QUANTUM DYNAMICS: TFIM Depth-Accuracy Analysis (Lie-Trotter)")
print("=" * 72)
print(f"Exact <Mz(t={time})> = {exact:+.6f}\n")
print(f"{'Steps':<7}{'<Mz(t)>':>12}{'|error|':>12}{'Depth':>8}   Error (log scale)")
print("-" * 72)

errors = []
for steps in trotter_steps_range:
    # FIX: pass the synthesis method into the gate instead of calling
    # synthesize() on gate.definition (a QuantumCircuit, not a gate).
    evo_gate = PauliEvolutionGate(hamiltonian, time=time, synthesis=LieTrotter(reps=steps))

    qc = QuantumCircuit(num_spins)
    qc.append(evo_gate, range(num_spins))
    qc = qc.decompose(reps=2)

    mz = float(estimator.run([(qc, magnetization_op)]).result()[0].data.evs)
    err = abs(mz - exact)
    errors.append(err)

    # Longer bar = larger error, on a log scale (1e-6 -> 0 chars, 1 -> 30 chars)
    bar_len = max(0, int((np.log10(max(err, 1e-12)) + 6) / 6 * 30))
    print(f"{steps:<7}{mz:>+12.6f}{err:>12.2e}{qc.depth():>8}   {'█' * bar_len}")

print("=" * 72)

# 8. Honest convergence check instead of a hardcoded success message
if errors[-1] < errors[0] and errors[-1] < 1e-3:
    print(f"Converged: error fell from {errors[0]:.2e} to {errors[-1]:.2e} "
          f"at {trotter_steps_range[-1]} steps.")
else:
    print("Not converged: increase Trotter steps or use a higher-order formula.")