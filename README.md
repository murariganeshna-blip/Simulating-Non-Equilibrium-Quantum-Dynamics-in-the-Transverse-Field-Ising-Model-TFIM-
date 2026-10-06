Project Title: Simulating Non-Equilibrium Quantum Dynamics in the Transverse-Field Ising Model (TFIM)   
PDF
Challenge Track: Track 5: Simulating Quantum Dynamics with the Transverse-Field Ising Model (BasQ Prompt)   
PDF
Overview
Simulating non-equilibrium quantum many-body dynamics is a leading pathway to demonstrating practical quantum utility. In this project, we construct digital quantum simulation circuits using Qiskit to model spin chains governed by the Transverse-Field Ising Model (TFIM) Hamiltonian, H=−J∑Z 
i
​	
 Z 
i+1
​	
 −h∑X 
i
​	
 . Because the interaction (H 
ZZ
​	
 ) and transverse field (H 
X
​	
 ) terms do not commute ([H 
ZZ
​	
 ,H 
X
​	
 ]

=0), the unitary time-evolution operator U(t)=e 
−iHt
  cannot be synthesized directly as single-step gates and must be discretized using product formulas.   
PDF
+ 4
Methodology & Qiskit Implementation
Using Qiskit SDK primitives, we mapped the spin chain Hamiltonian using SparsePauliOp and synthesized the unitary evolution operator U(t)≈(e 
−iH 
ZZ
​	
 Δt
 e 
−iH 
X
​	
 Δt
 ) 
r
  via PauliEvolutionGate and first-order LieTrotter product formulas. We tracked time-resolved expectation values for the average site magnetization ⟨M 
z
​	
 (t)⟩= 
N
1
​	
 ∑ 
i
​	
 ⟨Z 
i
​	
 (t)⟩ using Qiskit's StatevectorEstimator across increasing Trotter step counts (r∈[1,40]).   
PDF
+ 4
Key Results & Depth-Accuracy Trade-off
Our simulation successfully isolated and benchmarked the Trotter error against exact classical numerical baselines:   
PDF
+ 1
Error Suppression: Increasing Trotter steps from r=1 to r=40 systematically reduced algorithmic discretization error from 9.53×10 
−1
  down to 5.48×10 
−5
 .   
JPG
Optimal Depth-Accuracy Sweet Spot: We mapped the exact convergence trajectory relative to transpiled circuit depth (scaling up to depth 283 at 40 steps). This identifies the optimal step size Δt 
∗
  required to minimize total simulation error before hardware gate noise dominates on NISQ processors.   
PDF
+ 2
Significance
By evaluating quantum observable decay and error scaling, this work demonstrates how digital Trotterization on quantum hardware avoids the exponential state-space bottlenecks of classical matrix exponentiation, paving the way for scalable utility-scale Floquet dynamics and non-equilibrium quantum physics simulations.
