const recordBtn = document.getElementById('record-btn');
const startConvButton = document.getElementById('startConvButton');
const endConvButton = document.getElementById('endConvButton');
const chatContainer = document.getElementById('chatContainer');

let mediaRecorder;
let audioChunks = [];

recordBtn.addEventListener('mousedown', startRecording);
recordBtn.addEventListener('mouseup', stopRecording);

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
      mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
      mediaRecorder.start();
      })
      .catch(err => console.error(err));
}

function stopRecording() {
  if (mediaRecorder) {
    mediaRecorder.stop();

    mediaRecorder.onstop = () => {
    const blob = new Blob(audioChunks, { type: mediaRecorder.mimeType });
    sendAudioToFlask(blob);
    audioChunks = []; // Reset for next recording
    };
  }
}

function sendAudioToFlask(blob) {
  const formData = new FormData();
  formData.append('audio', blob, 'audio.webm');

  fetch('/record', {
      method: 'POST',
      body: formData
  })
  .then(response => {
      if (response.ok) {
          return response.json(); // Parse response as JSON
      } else {
          console.error('Error sending audio:', response.statusText);
      }
  })
  .then(data => {
    // Parse transcript as an array of objects
    const output = data.transcript.map(item => {
      return {
          user_messagee: item.user_messagee,
          agg_voice: item.agg_voice,
          agg_text: item.agg_text,
          resp: item.resp
      };
    });

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '<div class="message sender">Thank you for calling us, How can I help you?</div>';

    // Update transcript content
    output.forEach((item, index) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'receiver');

        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('user-message');
        userMessageElement.textContent = item.user_messagee;
        messageElement.appendChild(userMessageElement);

        const aggTextElement = document.createElement('div');
        aggTextElement.classList.add('agg-text');
        aggTextElement.textContent = `Agg Text: ${item.agg_text}`;

        const aggVoiceElement = document.createElement('div');
        aggVoiceElement.classList.add('agg-voice');
        aggVoiceElement.textContent = `Agg Voice: ${item.agg_voice}`;

        chatBox.appendChild(messageElement);
        chatBox.appendChild(aggTextElement);
        chatBox.appendChild(aggVoiceElement);

        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'sender');
        botMessageElement.textContent = item.resp;
        chatBox.appendChild(botMessageElement);
    });

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;

    // Update department content
    document.getElementById('department').textContent = data.dep;

    // Set source path for audio
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.src = `${data.audio_path}`;

    // if data have status
    if (data.status) {
      // if data.status is 'end', end the conversation
      if (data.status === "end") {
        document.getElementById('aggro').textContent = data.overall_sentiment;
        // Wait for 6 seconds
        setTimeout(() => {
          startConvButton.style.display = 'flex';
          endConvButton.style.display = 'none';
          chatContainer.style.display = 'none';
        }, 6000);
      }

      // if data.status is 'route'
      if (data.status === "route") {
        document.getElementById('aggro').textContent = data.overall_sentiment;
        document.getElementById('agent').textContent = data.agent_name;
        document.getElementById('position').textContent = data.position;
      }
    }
  })
  .catch(err => console.error('Error sending audio:', err));
}

startConvButton.addEventListener('click', () => {
  
  startConvButton.style.display = 'none';
  endConvButton.style.display = 'flex';
  chatContainer.style.display = 'block';
  document.getElementById('aggro').textContent = "";
  document.getElementById('agent').textContent = "";
  document.getElementById('department').textContent = "";
  document.getElementById('position').textContent = "";
  const chatBox = document.getElementById('chat-box');
  chatBox.innerHTML = '<div class="message sender">Thank you for calling us, How can I help you?</div>';
  
  // play welcome message audio
  const audioPlayer = document.getElementById('audioPlayer');
  audioPlayer.src = '/static/audio/welcome_message.mp3';
  
});

endConvButton.addEventListener('click', () => {
  startConvButton.style.display = 'flex';
  endConvButton.style.display = 'none';
  chatContainer.style.display = 'none';
  // create a get request to end the conversation
  fetch('/end-conversation', {
    method: 'POST'
  })
  .then(response => {
    if (response.ok) {
      return response.json(); // Parse response as JSON
    } else {
      throw new Error('Error ending conversation: ' + response.statusText);
    }
  })
  .then(data => {
    if (data.overall_sentiment) {
      document.getElementById('aggro').textContent = data.overall_sentiment;
    }
  })
  .catch(err => console.error('Error ending conversation:', err));
});