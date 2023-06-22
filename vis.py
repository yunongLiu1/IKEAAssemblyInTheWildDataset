import pandas as pd
import json
from PIL import Image
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
import os
from IPython.display import display
import matplotlib.pyplot as plt
import pandas as pd



def visualization(furniture_id, furniture_sub_category, video_id, page_index, step_index, start_time, end_time, json_data, row):
    # Load the manual page
    manual_path = f"./dataset/Furniture/{furniture_sub_category}/{furniture_id}/manual/1/page-{page_index}.png"
    image = Image.open(manual_path)

    # Load the cropped image
    step_path = f"./dataset/Furniture/{furniture_sub_category}/{furniture_id}/step/step-{step_index}.png"
    step_image = Image.open(step_path)

    # Load the video
    video_path = f"./dataset/Furniture/{furniture_sub_category}/{furniture_id}/video/{video_id}.mp4"
    video = VideoFileClip(video_path).subclip(start_time, end_time)
    # Save the video as a new file
    video.write_videofile("video.mp4", codec="libx264", audio_codec="aac")


    # Create a figure to hold the subplots
    plt.figure(figsize=(18, 6))  # adjust the size as needed

    # Add a subplot for the manual page
    plt.subplot(1, 3, 1)  # 1 row, 3 columns, first plot
    plt.imshow(image)
    plt.title(f"Page {page_index} of the manual")
    plt.axis('off')

    # Add a subplot for the cropped image
    plt.subplot(1, 3, 2)  # 1 row, 3 columns, second plot
    plt.imshow(step_image)
    plt.title(f"Step {step_index}")
    plt.axis('off')

    plt.tight_layout()  # adjust spacing between subplots to minimize the overlaps.
    plt.show()

    # Display the video separately (since matplotlib can't handle video)
    display(video.ipython_display(fps=24, loop=True, autoplay=True, rd_kwargs=dict(logger=None)))

    # Display other info
    print(f"Furniture ID: {furniture_id}")
    print(f"Furniture Subcategory: {row['furniture_sub_category'].values[0]}")
    print(f"Step List Length: {row['step_list_length'].values[0]}")
    print(f"Page List Length: {row['page_list_length'].values[0]}")
    print(f"Full Video Duration: {row['full_video_duration'].values[0]} seconds")

    # Find and display corresponding JSON data
    for furniture in json_data:
        if furniture['id'] == furniture_id:
            print(json.dumps(furniture, indent=4))
            break

# main
if __name__ == '__main__':
    
    # Load the CSV file
    csv_path = "./dataset/split/train_clip.csv"  # replace with your csv path
    df = pd.read_csv(csv_path)

    # Load the JSON file
    json_path = "./dataset/split/train.json"  # replace with your json path
    with open(json_path, "r") as f:
        json_data = json.load(f)


    # Pick a random row from the CSV
    sample_row = df.sample()

    # Extract info
    furniture_id = sample_row['furniture_id'].values[0]
    furniture_sub_category = sample_row['furniture_sub_category'].values[0]
    video_id = sample_row['video_id'].values[0]
    page_index = sample_row['page_index'].values[0] + 1 # The first page is 1 instead of 0
    step_index = sample_row['step_index'].values[0] + 1 # The first step is 1 instead of 0
    start_time = sample_row['start_time'].values[0]
    end_time = sample_row['end_time'].values[0]

    # Extract the rows with the same furniture ID, video ID, and step index
    same_step_index = df[(df['furniture_id'] == furniture_id) & (df['video_id'] == video_id) & (df['step_index'] == step_index)]


    # For each row, visualize the corresponding manual page, cropped image, and video
    for index, row in same_step_index.iterrows():
        visualization(furniture_id, furniture_sub_category, video_id, page_index, step_index, start_time, end_time, json_data, row)
        



