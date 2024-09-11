import yt_dlp
import os

def download_video(url, download_type='video', audio_format=None, output_dir='.'):
    # Verifica se o diretório de saída existe, caso contrário, cria-o
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Define o template para o nome do arquivo no diretório especificado
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s') if download_type == 'video' else os.path.join(output_dir, '%(title)s - %(artist)s.%(ext)s'),
        'restrictfilenames': False,  # Permite caracteres não-ASCII e espaços
    }

    if download_type == 'video':
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        })
    elif download_type == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
            }, {
                'key': 'FFmpegMetadata',  # Adiciona metadados ao arquivo de áudio
            }],
        })
        if audio_format == 'mp3':
            ydl_opts['postprocessors'][0]['preferredquality'] = '320'
    else:
        print("Opção de download inválida. Escolha 'video' ou 'audio'.")
        return

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'Unknown Title')
            if download_type == 'audio':
                artist = info_dict.get('artist', 'Unknown Artist')
                print(f"Download concluído: {title} - {artist}")
            else:
                print(f"Download concluído: {title}")
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")

if __name__ == "__main__":
    while True:
        # Solicita a URL do vídeo do YouTube
        url = input("Digite a URL do vídeo do YouTube: ").strip()
        
        if not url:
            print("Nenhuma URL fornecida. Encerrando o programa.")
            break
        
        # Solicita o tipo de download (vídeo ou áudio)
        while True:
            download_type = input("Você deseja baixar o vídeo ou apenas o áudio? (video/audio): ").strip().lower()
            if download_type in ['video', 'audio']:
                break
            print("Tipo de download inválido. Por favor, digite 'video' ou 'audio'.")
        
        # Solicita o diretório de saída
        output_dir = input("Digite o diretório de saída (padrão: output): ").strip() or 'output'

        if download_type == 'audio':
            # Solicita o formato de áudio desejado
            while True:
                audio_format = input("Qual formato de áudio você deseja? (mp3/wav): ").strip().lower()
                if audio_format in ['mp3', 'wav']:
                    break
                print("Formato de áudio inválido. Por favor, digite 'mp3' ou 'wav'.")
            download_video(url, download_type, audio_format, output_dir)
        else:
            download_video(url, download_type, output_dir=output_dir)
        
        # Pergunta ao usuário se deseja fazer outro download
        another_download = input("Deseja fazer outro download? (s/n): ").strip().lower()
        if another_download != 's':
            print("Encerrando o programa.")
            break
