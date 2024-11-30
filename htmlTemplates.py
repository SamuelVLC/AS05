css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://designerapp.officeapps.live.com/designerapp/document.ashx?path=/3603d64e-90cb-43fb-91c2-a0a7fbe62b82/DallEGeneratedImages/dalle-8c4cc0ff-2a66-4b44-91d3-6e29e0b197f00251682529505666472300.jpg&dcHint=BrazilSouth&fileToken=b50da40c-0b75-41f1-b65e-fcc602fe5be7" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://designerapp.officeapps.live.com/designerapp/document.ashx?path=/d107f6fb-6534-43e4-aa43-81afe8f130cc/DallEGeneratedImages/dalle-957a80d2-be2a-49fe-bae9-eb0d4dfed6db0251682527458694508400.jpg&dcHint=BrazilSouth&fileToken=2637644e-ca62-495b-9859-0c5afeba2ae8">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
