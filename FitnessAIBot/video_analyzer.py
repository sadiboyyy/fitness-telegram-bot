import os
import av


def extract_frames(video_path, output_folder="frames"):

    os.makedirs(output_folder, exist_ok=True)

    # Удаляем старые кадры предыдущего видео
    for filename in os.listdir(output_folder):
        if filename.endswith(".jpg"):
            os.remove(
                os.path.join(output_folder, filename)
            )

    container = av.open(video_path)

    stream = container.streams.video[0]

    fps = float(stream.average_rate)

    saved = 0

    # Один кадр примерно каждые 2 секунды
    frame_interval = max(
        int(fps * 2),
        1
    )

    for i, frame in enumerate(
        container.decode(stream)
    ):

        if i % frame_interval == 0:

            image = frame.to_image()

            image.save(
                os.path.join(
                    output_folder,
                    f"frame_{saved:03d}.jpg"
                )
            )

            saved += 1

            # Максимум 30 кадров
            if saved >= 30:
                break

    container.close()

    return saved