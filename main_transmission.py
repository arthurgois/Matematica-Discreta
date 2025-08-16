import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import Hamming
from Channel import bsc
import os

#Carrega uma imagem e converte para bits
def load_image_as_bits(image_path):
    try:
        img = Image.open(image_path).convert('L')  # tons de cinza
        img = img.resize((512, 512))
        img_array = np.array(img, dtype=np.uint8)
        
        # Converter cada pixel (8 bits) para sequência de bits
        bits = np.unpackbits(img_array.flatten())
        
        print(f"Imagem carregada: {img_array.shape}")
        print(f"Total de bits: {len(bits)}")
        
        return bits, img_array.shape
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")
        return None, None

# Reconstrói imagem a partir dos bits
def bits_to_image(bits, shape):
    try:
        # Garantir que temos o número correto de bits
        expected_bits = shape[0] * shape[1] * 8
        if len(bits) < expected_bits:
            # Padding com zeros se necessário
            bits = np.concatenate([bits, np.zeros(expected_bits - len(bits), dtype=np.uint8)])
        elif len(bits) > expected_bits:
            # Truncar se temos bits demais
            bits = bits[:expected_bits]
        
        bytes_array = np.packbits(bits).reshape(shape)
        return Image.fromarray(bytes_array, mode='L')
    except Exception as e:
        print(f"Erro ao reconstruir imagem: {e}")
        return None

# Transmissão sem codificação de canal
def transmit_uncoded(image_bits, EbN0_dB):
    R = 1  # taxa = 1 (todos os bits são de informação)
    
    # Transmitir pelo canal BSC
    received_bits, p = bsc(image_bits.copy(), EbN0_dB, R)
    
    # Calcular BER (bit error rate)
    errors = np.sum(image_bits != received_bits)
    ber = errors / len(image_bits)
    
    print(f"  Sem codificação - BER: {ber:.6f}, p teórico: {p:.6f}")
    
    return received_bits, ber, p

# Transmissão com codificação Hamming [7,4]
def transmit_coded(image_bits, EbN0_dB):
    R = 4/7  # taxa do código Hamming (4 bits info / 7 bits total)
    syn_table = Hamming.syndrome_table()
    
    # Fazer padding para múltiplo de 4 bits
    padding = (4 - len(image_bits) % 4) % 4
    if padding > 0:
        padded_bits = np.concatenate([image_bits, np.zeros(padding, dtype=np.uint8)])
    else:
        padded_bits = image_bits.copy()
    
    # Codificar em blocos de 4 bits
    coded_bits = []
    for i in range(0, len(padded_bits), 4):
        block = padded_bits[i:i+4]
        coded_block = Hamming.encode(block)
        coded_bits.extend(coded_block)
    
    coded_bits = np.array(coded_bits, dtype=np.uint8)
    
    print(f"  Bits originais: {len(image_bits)}, Codificados: {len(coded_bits)}")
    
    # Transmitir pelo canal BSC
    received_coded, p = bsc(coded_bits, EbN0_dB, R)
    
    # Decodificar bloco por bloco
    decoded_bits = []
    corrected_errors = 0
    
    for i in range(0, len(received_coded), 7):
        received_block = received_coded[i:i+7]
        corrected_block, decoded_block, error_info = Hamming.decode(received_block, syn_table)
        decoded_bits.extend(decoded_block)
        
        if error_info != "no error":
            corrected_errors += 1
    
    decoded_bits = np.array(decoded_bits, dtype=np.uint8)
    
    # Remover padding
    if padding > 0:
        decoded_bits = decoded_bits[:-padding]
    
    # Calcular BER
    errors = np.sum(image_bits != decoded_bits)
    ber = errors / len(image_bits)
    
    print(f"  Com codificação - BER: {ber:.6f}, Blocos corrigidos: {corrected_errors}")
    
    return decoded_bits, ber, p

# Executa simulação completa
def run_simulation(image_path):
    # Carregar imagem
    image_bits, img_shape = load_image_as_bits(image_path)
    if image_bits is None:
        print("Erro: não foi possível carregar a imagem")
        return
    
    # Parâmetros da simulação
    EbN0_range = np.arange(0, 11, 1)
    ber_uncoded = []
    ber_coded = []
    p_theoretical = []
    
    # Pontos para salvar imagens
    save_points = [0, 2, 4, 5, 6, 7, 8, 10]
    
    print("Iniciando simulação...")
    
    filename = os.path.splitext(os.path.basename(image_path))[0]

    for EbN0 in EbN0_range:
        print(f"\nSimulando Eb/N0 = {EbN0} dB...")
        
        # Transmissão sem codificação
        received_uncoded, ber_unc, p_theo = transmit_uncoded(image_bits, EbN0)
        ber_uncoded.append(ber_unc)
        p_theoretical.append(p_theo)
        
        # Transmissão com codificação
        received_coded, ber_cod, _ = transmit_coded(image_bits, EbN0)
        ber_coded.append(ber_cod)
        
        # Salvar imagens para pontos específicos
        if EbN0 in save_points:
            print(f"  Salvando imagens para Eb/N0 = {EbN0} dB...")
            
            # Reconstruir e salvar imagem sem codificação
            img_unc = bits_to_image(received_uncoded, img_shape)
            if img_unc:
                img_unc.save(f'imgs_uncoded/{filename}_uncoded_{EbN0}dB.png')
            
            # Reconstruir e salvar imagem com codificação
            img_cod = bits_to_image(received_coded, img_shape)
            if img_cod:
                img_cod.save(f'imgs_coded/{filename}_coded_{EbN0}dB.png')
    
    # Plotar curvas de desempenho
    plt.figure(figsize=(10, 6))
    plt.semilogy(EbN0_range, p_theoretical, 'b-', linewidth=2, label='Theoretical values')
    plt.semilogy(EbN0_range, ber_uncoded, 'ro', markersize=6, label='Uncoded (simulation)')
    plt.semilogy(EbN0_range, ber_coded, 'gs', markersize=6, label='Coded (simulation)')
    
    plt.xlabel('$E_b/N_0$ (dB)', fontsize=14)
    plt.ylabel('BER', fontsize=14)
    plt.grid(True, which='both', linestyle=':', alpha=0.5)
    plt.legend(fontsize=12)
    plt.title('BER Performance Comparison', fontsize=14)
    plt.ylim([1e-5, 1])

    plt.show()
    
    print("\nSimulação concluída!")
    print("Arquivos gerados:")
    for EbN0 in save_points:
        print(f"- {filename}_uncoded_{EbN0}dB.png")
        print(f"- {filename}_coded_{EbN0}dB.png")


if __name__ == "__main__":   
    # Execute a simulação
    image_path = '.\imgs_banco\CTG.png'     # Imagem do CTG
    #image_path = '.\imgs_banco\Lena.png'   # Imagem da Lena
    
    try:
        run_simulation(image_path)
    except Exception as e:
        print(f"Erro durante a simulação: {e}")
        print("Verifique se:")
        print("1. Os módulos Hamming.py e Channel.py estão no mesmo diretório")
        print("2. A imagem especificada existe")
        print("3. As dependências estão instaladas corretamente")