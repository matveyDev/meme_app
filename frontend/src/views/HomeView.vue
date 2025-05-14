<template>
  <div class="home">
    <div class="crypto-background"></div>
    <div class="crypto-background-overlay"></div>

    <!-- MAKE MEME Button -->
    <button class="make-meme">
      MAKE MEME
    </button>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style>
/* Global background styles */
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  background: #111;
  overflow: hidden;
  font-family: 'Orbitron', sans-serif;
}

#app {
  height: 100%;
  background: transparent;
  overflow: hidden;
}

/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&display=swap');

.home {
  width: 100%;
  height: 100%;
  color: #ffffff;
  position: fixed;
  overflow: hidden;
}

.crypto-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('@/assets/background.jpg') center/cover no-repeat;
  z-index: 0;
  pointer-events: none;
}

.crypto-background::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 255, 102, 0.1), rgba(255, 64, 129, 0.1));
  z-index: 1;
  pointer-events: none;
}

.crypto-background::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-size: 250px 250px;
  z-index: 2;
  opacity: 0.4;
  pointer-events: none;
  animation: starFloat 60s linear infinite;
}

/* MAKE MEME Button */
.make-meme {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-family: 'Orbitron', sans-serif;
  font-size: 28px;
  font-weight: 900;
  background-color: #00FF66;
  color: #FF4081;
  border: 4px solid #00cc55;
  padding: 25px 50px;
  text-shadow: 0 0 10px #FF4081, 0 0 20px #FF4081;
  box-shadow: 0 0 15px #00FF66, 0 0 30px rgba(0, 255, 102, 0.5);
  z-index: 11;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 3px;
  text-transform: uppercase;
  border-radius: 8px;
  background: linear-gradient(45deg, #00FF66, #00cc55);
  animation: glow 2s ease-in-out infinite alternate;
  display: none; /* Temporarily hide button */
}

.make-meme:hover {
  transform: translate(-50%, -50%) scale(1.05);
  box-shadow: 0 0 25px #00FF66, 0 0 50px rgba(0, 255, 102, 0.7);
  color: #FF4081;
  text-shadow: 0 0 15px #FF4081, 0 0 30px #FF4081;
  background: linear-gradient(45deg, #00FF66, #00cc55, #00FF66);
  animation: glow 1s ease-in-out infinite alternate;
}

.make-meme:active {
  transform: translate(-50%, -50%) scale(0.95);
  box-shadow: 0 0 10px #00FF66, 0 0 20px rgba(0, 255, 102, 0.3);
}

@keyframes glow {
  from {
    box-shadow: 0 0 15px #00FF66, 0 0 30px rgba(0, 255, 102, 0.5);
    text-shadow: 0 0 10px #FF4081, 0 0 20px #FF4081;
  }
  to {
    box-shadow: 0 0 25px #00FF66, 0 0 50px rgba(0, 255, 102, 0.7);
    text-shadow: 0 0 15px #FF4081, 0 0 30px #FF4081;
  }
}

/* Animations */
@keyframes starFloat {
  0% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0); }
}

/* Responsiveness */
@media (max-width: 600px) {
  .content-wrapper {
    padding: 16px;
    border-radius: 16px;
  }
}
</style> 