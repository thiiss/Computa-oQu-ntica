try:
    from qiskit import QuantumCircuit
    from qiskit_aer import Aer
    from qiskit.visualization import plot_histogram
except ImportError:
    print("Instalando Qiskit...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qiskit", "qiskit-aer"])
    from qiskit import QuantumCircuit
    from qiskit_aer import Aer
    from qiskit.visualization import plot_histogram

import matplotlib.pyplot as plt

# Restante do seu código aqui...
class SensorIoT:
    def __init__(self, nome, estado):
        self.nome = nome
        self.estado = estado

def criar_circuito(sensores):
    qc = QuantumCircuit(2, 2)
    if sensores[0].estado == 1:
        qc.x(0)
    if sensores[1].estado == 1:
        qc.x(1)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc

def simular_cenarios():
    cenarios = [
        [SensorIoT("Fumaça", 0), SensorIoT("Obstrução", 0)],
        [SensorIoT("Fumaça", 1), SensorIoT("Obstrução", 0)],
        [SensorIoT("Fumaça", 0), SensorIoT("Obstrução", 1)],
        [SensorIoT("Fumaça", 1), SensorIoT("Obstrução", 1)]
    ]
    
    print("=== RESULTADOS ===")
    for idx, cenario in enumerate(cenarios, 1):
        qc = criar_circuito(cenario)
        simulator = Aer.get_backend('qasm_simulator')
        result = simulator.run(qc, shots=1000).result()
        counts = result.get_counts()
        
        if idx == 1:
            print("Cenário 01 - ✅ Rota Principal Segura")
        elif idx == 2:
            print("Cenário 02 - ⬅️ Rota Alternativa 1")
        elif idx == 3:
            print("Cenário 03 - ➡️ Rota Alternativa 2")
        else:
            print("Cenário 04 - 🚨 Nenhuma rota segura")
        
        print(f"Contagens: {counts}\n")

if __name__ == "__main__":
    simular_cenarios()