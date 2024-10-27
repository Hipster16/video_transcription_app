import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def get_transcription(file_name: str) -> str:
  genai.configure(api_key=os.environ["GEMINI_API_KEY"])
  # Create the model
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
  # system_instruction="""Detect the language in the audio file that i provided and transcribe it to english along with the time stamp. give the transcribe text and timestamp ONLY. do not give any other explaination.
  # sample output
  # 00:00 Hello, because the international football,  \n00:02 tomorrow will be the deadline, free,  \n00:05 Then a lot of people are  \n00:07 release the three aspects of the research,  \n00:11 research more difficult,  \n00:13 screen inside,  \n00:15 test, I myself,  \n00:17 more careful,  \n00:21 dynamic images  \n00:23 interpretation to everyone,  \n00:26 stage conclusion to  \n00:28 Let international friends  \n00:30 If tonight or  \n00:32 morning brush  \n00:33 some reference. First is about the  \n00:36 point is,  \n00:38 and speed together to  \n00:40 fast break speed and feel,  \n00:43 means kicking frequency,  \n00:46 ratio is,  \n00:48 Inside the negative point is the speed,  \n00:51 can affect the ball's accuracy.  \n00:54 Maybe will think that the speed,  \n00:56 with skills,  \n00:58 1.1, so-called,  \n01:00 break, from  \n01:03 accelerate 15 m, then,  \n01:05 slow down  \n01:07 press the  \n01:10 press and then forward  \n01:12 accelerating, then accelerate to  \n01:13 extreme state,  \n01:15 need 12m.  \n01:17 For what time  \n01:19 will reach the extreme state,  \n01:22 I'm talking about the  \n01:24 nature is,  \n01:26 players make corresponding movements,  \n01:28 the time, is a  \n01:30 time,  \n01:32 frequency.  \n01:33 According to the test,  \n01:35 players kicking time,  \n01:37 longer,  \n01:39 then players in the dribbling  \n01:41 the ball, the passing, the dribbling  \n01:43 then need  \n01:44 more time,  \n01:46 the movement.  \n01:48 Understand the movement,  \n01:51 1.4, kicking frequency  \n01:53 higher,  \n01:54 the ball's  \n01:56 the body is closer,  \n01:58 players execute different  \n01:59 instructions will be faster.  \n02:02 Avoid the defense player,  \n02:04 from the sideline  \n02:06 the ball is close.  \n02:07 1.5, after the test,  \n02:10 height can be  \n02:11 equal to 1 dribbling,  \n02:14 contribution.  \n02:15 1.6, can see,  \n02:17 thinking is,  \n02:19 simply put the  \n02:22 according to a certain internal  \n02:23 ratio, calculate a  \n02:25 corresponding  \n02:26 dribbling fast break.  \n02:28 The game don't for  \n02:30 low skill  \n02:31 players specifically,  \n02:33 dribbling fast, but the  \n02:34 kicking frequency low, feel bad  \n02:36 performance. This  \n02:38 is for simplifying  \n02:40 the design work.  \n02:42 This also led to the speed  \n02:44 dribbling skill better,  \n02:45 this sounds weird,  \n02:47 regarding the score,  \n02:49 the table shows,  \n02:51 they both  \n02:52 reach 190, then  \n02:54 improve kicking or speed, then for  \n02:57 dribbling fast break  \n02:59 performance, the increase will  \n03:01 significantly decrease score.  \n03:03 This is the  \n03:05 99, speed 99, only  \n03:07 99, speed 90,  \n03:10 0.5,  \n03:12 frequency doesn't  \n03:14 significantly high,  \n03:16 is simply for  \n03:18 pursue speed  \n03:21 100, one is 99, one is 90, score  \n03:24 will be better.  \n03:25 Second point, kicking is the effect  \n03:27 dribbling's start  \n03:29 the speed, can think that press,  \n03:31 kick the ball,  \n03:32 kicking start to effect,  \n03:34 won't wait till  \n03:35 fast break state,  \n03:36 2.1, have another  \n03:38 factor,  \n03:40 skill is close ball control,  \n03:42 but close ball control for  \n03:44 dribbling's start,  \n03:46 kicking's half,  \n03:47 2.2, 2.3,  \n03:49 speed and acceleration don't  \n03:51 dribbling start section.  \n03:53 Second big point, ball control, first point, ball control effect is the  \n03:56 stop and fake, second point,  \n03:58 after the contact, immediately  \n04:00 dribbling start  \n04:01 operation, ball control will  \n04:02 to start speed  \n04:04 effect,  \n04:06 ball control's effect in  \n04:08 faster, more spinning,  \n04:10 will be bigger,  \n04:12 if receive the ball  \n04:14 slower,  \n04:16 ball control effect will be smaller,  \n04:18 Third,  \n04:20 point,  \n04:22 can be divided into two parts,  \n04:24 dribbling  \n04:26 dribbling frequency,  \n04:28 I'm describing for  \n04:30 a bit strict,  \n04:32 dribbling  \n04:34 this turning,  \n04:36 slow down dribbling,  \n04:38 the direction and the direction  \n04:40 smaller than 15 degree,  \n04:42 just like in the picture this,  \n04:44 state.  \n04:45 This state has a  \n04:46 meaningful point,  \n04:48 kicking frequency is affected by close ball control, but  \n04:51 close ball control smaller than 70,  \n04:53 higher than 82, then  \n04:55 kicking frequency is locked,  \n04:56 all the same.  \n04:58 Specifically, below 70  \n05:01 frequency is slower than 82 or above,  \n05:03 in other words, only  \n05:05 close ball control 70 to 82,  \n05:07 then,  \n05:08 a bit more effort to increase, will bring  \n05:11 kicking frequency's actual effect. However,  \n05:14 decrease can be consider as  \n05:16 increase the  \n05:18 kicking frequency.  \n05:20 close ball control,  \n05:21 then need  \n05:23 close ball control  \n05:24 kicking frequency will be higher, feel  \n05:26 better.  \n05:27 So, game  \n05:29 low speed  \n05:30 the small  \n05:32 dribbling feel, not  \n05:34 a high  \n05:36 close ball control,  \n05:37 can be  \n05:39 see and achieve.  \n05:40 3.1, self see the words.  \n05:42 Simply that piece dribbling  \n05:44 turning movement,  \n05:46 not include  \n05:48 before the turning,  \n05:50 kicking frequency,  \n05:51 is unrelated to height.  \n05:53 So high players can  \n05:55 execute  \n05:57 large  \n05:59 the turning movement.  \n06:01 And no data restriction.  \n06:03 This  \n06:05 look at the picture  \n06:06 display  \n06:08 screen.  \n06:10 3.3,  \n06:12 meaningful,  \n06:14 kick the ball,  \n06:16 generally speaking,  \n06:18 a certain  \n06:20 situation,  \n06:22 180 degree  \n06:24 turning,  \n06:26 close ball control  \n06:28 more than 86 will be a  \n06:30 threshold,  \n06:32 the explanation.  \n06:34 Fourth point is,  \n06:36 affect high speed dribbling speed, include  \n06:38 kicking frequency.  \n06:40 But will affect  \n06:42 high speed dribbling whether to use  \n06:44 dominant foot.  \n06:46 See,  \n06:48 the state, left foot right foot left foot right foot basically is,  \n06:52 Then close ball control more than 90, is  \n06:54 using it's dominant foot,  \n06:55 kicking.  \n06:57 Use the weak foot.  \n06:59 The difference  \n07:01 main effect is,  \n07:03 high speed dribbling whether  \n07:05 conveniently use dominant foot kicking.  \n07:07 5th point, self see. Sixth point is the  \n07:10 special,  \n07:12 the press  \n07:14 the initial speed and feel see  \n07:17 close ball control value, not the  \n07:18 dribbling value.  \n07:20 The video is a bit rush,  \n07:22 hope to  \n07:23 help.  \n07:25 detailed, more specific official  \n07:27 with everyone,  \n07:29 See you later.  \n07:30 Bye. \n
  # """,
  system_instruction="""
    give me a detailed summary of the topics that is discussed. I want the output to be summary of the text that is being said and the time intervals in the video at with that is mentioned.
    sample output

0:00 - 0:35: Introduction and Overview

 The speaker introduces the topic of the video: an analysis of the impact of various game mechanics on dribbling in FIFA.
 He mentions that the free trial for FIFA is ending soon and that he's releasing his analysis. 
 He notes the complexity of the analysis and that he is trying to present the most crucial conclusions in a clear and concise way.
 He wants to help viewers understand the key factors that influence dribbling.

0:36 - 1:00: Dribbling Speed and Touch

 0:36 - 0:37: The first point is that dribbling speed and touch are both essential.
 0:38 - 0:41: The speaker explains that a player's touch when dribbling plays a significant role.
 0:42 - 0:46: He emphasizes that the frequency of a player's touch is more important than speed, giving a ratio of 5:4.
 0:47 - 0:52: The speaker explains that dribbling speed can indirectly affect the accuracy of the dribble. 
 0:53 - 1:00: He explains that the game's design prioritizes touch over speed and that the "speed burst" mechanic is more about quick acceleration than actual top speed. 

1:01 - 1:20: Dribbling Speed Burst

 1:01 - 1:10: The speaker describes the mechanics of how a player accelerates in the game, including the difference between "slow dribbling" and "fast dribbling."
 1:11 - 1:16: He explains that the distance a player needs to reach full speed is shorter than the distance needed to reach top speed.
 1:17 - 1:20: The speaker emphasizes that a player's touch and reaction time are crucial for reaching top speed. 

1:21 - 1:37: Touch Frequency and Dribbling Skill

 1:21 - 1:23:  He explains that touch frequency influences the responsiveness of the dribble.
 1:24 - 1:29: The speaker defines the "touch frequency" as the time it takes the player to react to the controls.
 1:30 - 1:32: The speaker explains that this reaction time affects how a player can perform other actions.
 1:33 - 1:37:  He explains that a longer touch frequency means longer reaction times, which can lead to slower reactions in various situations.

1:38 - 2:00: Touch Frequency, Reaction Time, and Responsiveness

 1:38 - 1:49: The speaker connects touch frequency with a player's ability to perform various actions like passing, tackling, and changing direction while dribbling.
 1:50 - 1:52: The speaker re-emphasizes that touch frequency plays a vital role in the feel of dribbling.
 1:53 - 1:59: He explains that a higher touch frequency makes dribbling faster and more responsive.
 2:00 - 2:02: Higher touch frequency also helps the player to be more agile and avoid interceptions.

2:03 - 2:14: Touch Frequency and Player Height

 2:03 - 2:10: The speaker explains that player height affects touch frequency, even at the same "touch" statistic. 
 2:11 - 2:14: He suggests that taller players benefit more from higher touch frequencies. 

2:15 - 2:28: Game Design and Dribbling Speed

 2:15 - 2:17: The speaker highlights the game's design philosophy for dribbling. 
 2:18 - 2:22: He explains that the game's engine simply combines speed and dribbling statistics into a single number that governs dribbling.
 2:23 - 2:27: He notes that the game doesn't have a separate mechanic for players with high speed but low touch or vice versa. 
 2:28 - 2:31: The speaker acknowledges that this design simplifies the game but leads to odd results.
  """  
  )
  files = [
    upload_to_gemini(f"downloads/{file_name}", mime_type="audio/mpeg"),
  ]

  chat_session = model.start_chat()

  response = chat_session.send_message(files[0])
  return response.text