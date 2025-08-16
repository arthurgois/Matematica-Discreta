# Simulação de Transmissão de Imagem com Codificação de Canal

##  Visão Geral do Projeto

Este projeto implementa um simulador de sistema de comunicação digital para transmissão de imagens utilizando código corretor de erros Hamming (7,4,3) através de um Canal Binário Simétrico (BSC). O sistema demonstra o comportamento paradoxal de códigos corretores simples em ambientes com alto ruído.

**Disciplina:** Matemática Discreta  
**Professor:** José Sampaio  
**Autor:** Arthur de Gois Santos  
**Instituição:** Universidade Federal de Pernambuco (UFPE)

##  Principais Características

- **Transmissão dual:** Comparação entre sistemas codificado e não codificado
- **Implementação Hamming (7,4,3):** Capacidade de correção de 1 bit por bloco
- **Simulação de canal BSC:** Relação sinal-ruído (Eb/N0) configurável
- **Avaliação visual:** Geração automática de imagens para múltiplos valores de SNR
- **Métricas de desempenho:** Cálculo de BER e comparação teórico vs. simulado
- **Visualização em tempo real:** Curvas de desempenho BER vs Eb/N0

##  Início Rápido

### Pré-requisitos

```bash
pip install numpy matplotlib pillow scipy
```

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/arthurgois/Matematica-Discreta.git
cd Matematica-Discreta
```

2. Certifique-se de que a seguinte estrutura de diretórios existe:
```
projeto/
│
├── main_transmission.py     # Script principal de simulação
├── Hamming.py               # Implementação do código Hamming
├── Channel.py               # Modelo do canal BSC
├── to_gray.py              # Utilitário de pré-processamento
│
├── imgs_banco/             # Diretório de imagens fonte
├── imgs_coded/             # Saída: resultados com codificação
├── imgs_uncoded/           # Saída: resultados sem codificação
├── imgs_banco_gray/        # Imagens convertidas para grayscale
└── img_to_gray/            # Entrada para conversão grayscale
```

### Executando a Simulação

#### Opção 1: Imagem Padrão (foto do CTG)
```bash
python main_transmission.py
```

#### Opção 2: Imagem Personalizada
1. Coloque sua imagem no diretório `imgs_banco/`
2. Edite a linha 179 em `main_transmission.py`:
```python
image_path = './imgs_banco/sua_imagem.png'
```
3. Execute a simulação:
```bash
python main_transmission.py
```

##  Descrição dos Módulos

### Módulos Principais

| Módulo | Descrição | Funções Principais |
|--------|-----------|-------------------|
| `main_transmission.py` | Orquestrador principal da simulação | `run_simulation()`, `transmit_coded()`, `transmit_uncoded()` |
| `Hamming.py` | Implementação do codec Hamming (7,4,3) | `encode()`, `decode()`, `syndrome()` |
| `Channel.py` | Simulador de canal BSC | `bsc()` - retorna bits com ruído e BER teórico |
| `to_gray.py` | Utilitário de pré-processamento | Converte imagens para 512×512 em tons de cinza |

### Especificação de Entrada/Saída

**Requisitos de Entrada:**
- Formato: PNG, JPEG ou qualquer formato suportado pela PIL
- Processamento: Redimensionada automaticamente para 512×512 pixels
- Espaço de cor: Convertida para 8-bit grayscale

**Saída Gerada:**
- 16 arquivos PNG (2 por ponto SNR): versões codificada e não codificada
- Gráfico de desempenho BER
- Log detalhado no terminal com métricas

##  Métricas de Desempenho

A simulação avalia:
- **BER (Taxa de Erro de Bit):** Fração de bits recebidos incorretamente
- **Ganho de Codificação:** 10×log₁₀(BER_sem/BER_com) dB
- **Blocos Corrigidos:** Número de blocos de 7 bits corrigidos com sucesso
- **Ponto de Crossover:** Eb/N0 ≈ 5.8 dB (onde a codificação se torna benéfica)

##  Parâmetros da Simulação

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| Tamanho da Imagem | 512×512 pixels | Dimensão padrão de teste |
| Bits por Pixel | 8 | Profundidade em grayscale |
| Total de Bits | 2.097.152 | Dados completos da imagem |
| Taxa do Código | 4/7 | Eficiência do Hamming (7,4,3) |
| Faixa Eb/N0 | 0-10 dB | Intervalo de varredura SNR |
| Pontos de Salvamento | [0,2,4,5,6,7,8,10] dB | Pontos de saída de imagem |

##  Saída Esperada no Terminal

```
Imagem carregada: (512, 512)
Total de bits: 2097152
Iniciando simulação...

Simulando Eb/N0 = 0 dB...
  Sem codificação - BER: 0.078682, p teórico: 0.078650
  Bits originais: 2097152, Codificados: 3670016
  Com codificação - BER: 0.119443, Blocos corrigidos: 339200
  Salvando imagens para Eb/N0 = 0 dB...

[... continua para todos os valores de SNR ...]

Simulação concluída!
```

##  Solução de Problemas

### Problemas Comuns e Soluções

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError` | Instale dependências faltantes: `pip install numpy matplotlib pillow scipy` |
| `FileNotFoundError` | Verifique o caminho da imagem e estrutura de diretórios |
| `ValueError: Error probability` | Verifique a faixa de Eb/N0 (deve ser positiva) |
| Diretórios de saída vazios | Crie os diretórios manualmente ou execute com privilégios de admin |

### Checklist de Debug
- [ ] Todos os pacotes Python necessários instalados
- [ ] Estrutura de diretórios criada corretamente
- [ ] Arquivo de imagem existe no caminho especificado
- [ ] Hamming.py e Channel.py na raiz do projeto
- [ ] Permissões de escrita para diretórios de saída

##  Fundamentação Técnica

### Código Hamming (7,4,3)
- **Matriz Geradora:** G = [P | I₄] onde P é a matriz de paridade
- **Matriz de Verificação:** H = [I₃ | P^T]
- **Distância Mínima:** d_min = 3
- **Correção de Erros:** t = 1 bit por bloco de 7 bits

### Canal Binário Simétrico (BSC)
- **Probabilidade de Erro:** p = 0.5 × erfc(√(R×Eb/N0))
- **Capacidade do Canal:** C = 1 - H(p) bits/uso do canal
- **Erros Simétricos:** P(0→1) = P(1→0) = p

##  Licença

Este projeto foi desenvolvido para fins acadêmicos como parte da disciplina de Matemática Discreta na UFPE.

##  Autor

**Arthur de Gois Santos**  
Universidade Federal de Pernambuco  
Departamento de Eletrônica e Sistemas  
Contato: arthur.gois@ufpe.br
---