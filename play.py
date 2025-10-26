from gtts import gTTS
from playsound import playsound
audio=" output.mp3"
language='en'
sing=gTTS(text='''hello thor your program is running succesfully . Good morning//everyone:My name is Gandham Uday Kiran,    and I am delighted to have the opportunity to introduce myself to you today.  I am (came)from the beautiful coastal city of Visakhapatnam  .I (came from) have a strong educational background
i recently completed my Bachelor's degree in Electrical and Electronics Engineering (EEE) from Sanketika Vidya Parishad Engineering College. And I scored 8.99 CGPA  I pursued (did)
 Diploma in Electrical Engineering from Behera Polytechnic Institute, where I graduated with an  85% score.

○My educational journey began at Ravindra Bharathi School in Visakhapatnam, where I had scored  10 GPA in my 10th standard


Along with my educational journey, I have developed strong communication skills, . Effective communication allows me to collaborate effectively with team members, present ideas confidently.

In addition to communication, I have also honed my technical skills.
-- I am good at programming languages such as Python
--web development technologies like HTML, CSS, 
--.I have a good knowledge on Basics  MySql.
And I am interested in learning latest technology so I started learn AWS cloud services,
And I am good at creating interact to dashboards in power bi
Coming to my Extra curricular activities  I had been this sports coordinators in my college .

 I am a quick learner, able to grasp new concepts rapidly. And iam a highly self motivated person .  
My hobbies include :
listing and singing music

watch movies  

playing cricket.

My goal is to secure a good job where I can grow professionally and contribute to the growth and success of the organization."and 
I want to make my parents proud of me ...

That's all about me sir thanks you


   ''',lang=language, slow=False)
sing.save(audio)
playsound(audio)

print("====audio is playing")
