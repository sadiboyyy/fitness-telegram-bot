import os
import av


def extract_frames(video_path, output_folder="frames"):

    os.makedirs(output_folder, exist_ok=True)

    container = av.open(video_path)

    stream = container.streams.video[0]

    fps = float(stream.average_rate)

    saved = 0

    for i, frame in enumerate(container.decode(stream)):

        # сохраняем кадр каждые 5 секунд
        if i % int(fps * 5) == 0:

            image = frame.to_image()

            image.save(
                os.path.join(
                    output_folder,
                    f"frame_{saved}.jpg"
                )
            )

            saved += 1

    return saved