from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

# 1. Modelo Simbólico dos Estados dos Sensores
class SensorIoT:
    def __init__(self, nome, estado):
        self.nome = nome  # Ex: "Fumaça", "Temperatura", "Obstrução"
        self.estado = estado  # 0 (seguro) ou 1 (perigoso)

# 2. Circuito Quântico para Tomada de Decisão
def circuito_evacuacao(sensores):
    qc = QuantumCircuit(3, 2)  # 3 qubits (2 para sensores + 1 para decisão)
    
    # Codificação dos dados dos sensores nos qubits
    for i, sensor in enumerate(sensores[:2]):  # Usando 2 sensores principais
        if sensor.estado == 1:  # Se sensor detecta perigo
            qc.x(i)  # Aplica porta X (Pauli-X)
    
    # Superposição para explorar múltiplos caminhos
    qc.h(0)  # Porta Hadamard no primeiro sensor
    qc.h(1)  # Porta Hadamard no segundo sensor
    
    # Entrelaçamento para correlação entre sensores
    qc.cx(0, 2)  # CNOT: qubit 0 controla o qubit 2 (decisão)
    qc.cx(1, 2)  # CNOT: qubit 1 também influencia a decisão
    
    # Medição apenas dos qubits de decisão
    qc.measure([0, 2], [0, 1])  # Mede caminho (0) e decisão (2)
    
    return qc

# 3. Simulação com Diferentes Cenários
def simular_cenarios():
    # Cenários de teste
    cenarios = [
        [SensorIoT("Fumaça", 0), SensorIoT("Obstrução", 0)],  # Tudo seguro
        [SensorIoT("Fumaça", 1), SensorIoT("Obstrução", 0)],  # Fumaça detectada
        [SensorIoT("Fumaça", 0), SensorIoT("Obstrução", 1)],  # Caminho bloqueado
        [SensorIoT("Fumaça", 1), SensorIoT("Obstrução", 1)]   # Ambos perigosos
    ]
    
    # Simular cada cenário
    for i, cenario in enumerate(cenarios):
        print(f"\n=== Cenário {i+1} ===")
        print(f"Sensor Fumaça: {'Perigo' if cenario[0].estado else 'Seguro'}")
        print(f"Sensor Obstrução: {'Perigo' if cenario[1].estado else 'Seguro'}")
        
        qc = circuito_evacuacao(cenario)
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=1000).result()
        counts = result.get_counts(qc)
        
        # Visualização
        print("\nDistribuição de Probabilidades:")
        display(plot_histogram(counts))
        
        # Interpretação dos resultados
        print("\nRecomendação de Evacuação:")
        if '00' in counts and counts['00'] > 600:  # 60% de chance
            print("✅ Rota Principal Segura")
        elif '01' in counts and counts['01'] > 600:
            print("⚠️ Usar Rota Alternativa 1")
        elif '10' in counts and counts['10'] > 600:
            print("⚠️ Usar Rota Alternativa 2")
        else:
            print("🚨 EVACUAÇÃO DE EMERGÊNCIA! Usar saídas alternativas")

# 4. Executar a simulação
simular_cenarios()
