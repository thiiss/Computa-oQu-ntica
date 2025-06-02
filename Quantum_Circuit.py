# Importando as bibliotecas necessárias
from qiskit import QuantumCircuit, execute, Aer
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# Criando um circuito quântico com 2 qubits
circuit = QuantumCircuit(2)

# Aplicando a porta Hadamard no primeiro qubit
circuit.h(0)

# Aplicando a porta CNOT, onde o primeiro qubit controla o segundo
circuit.cx(0, 1)

# Adicionando uma porta Pauli (X) para simular bloqueios em um dos caminhos
# Aqui vamos aplicar a porta X no segundo qubit, simulando um caminho bloqueado
circuit.x(1)

# Medindo os qubits
circuit.measure_all()

# Desenhando o circuito
circuit.draw('mpl')
plt.show()

# Simulando o circuito
simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend=simulator, shots=1024).result()
counts = result.get_counts(circuit)

# Exibindo os resultados
print("Contagem de resultados:", counts)

# Plotando o histograma dos resultados
plot_histogram(counts)
plt.show()
