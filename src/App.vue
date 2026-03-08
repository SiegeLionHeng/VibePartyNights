<template>
  <div class="app-container">
    <div class="header">
      <img src="/pic/组 22.png" class="header-img" />
    </div>
    <div class="schedule-list">
      <div 
        v-for="(day, dayIndex) in scheduleData" 
        :key="dayIndex"
        class="schedule-card"
        :style="{ backgroundImage: 'url(' + day.bgImage + ')' }"
      >
        <p class="date-text" :class="{ white: day.whiteText }">>>> {{ day.date }}</p>
        <div class="schedule-items">
          <div 
            v-for="(item, index) in day.items" 
            :key="index" 
            class="schedule-item"
            @click="handleItemClick"
          >
            <div class="item-row">
              <div class="time-block">
                <div class="dot" :class="{ white: day.whiteText }"></div>
                <span class="time-text" :class="{ white: day.whiteText }">{{ item.time }}</span>
              </div>
              <span class="location" :class="{ white: day.whiteText }">{{ item.location }}</span>
            </div>
            <div class="item-row">
              <span class="activity" :class="{ white: day.whiteText }" v-html="item.activity"></span>
              <span class="signup" :class="{ white: day.whiteText }">{{ item.signup }}</span>
            </div>
            <div class="divider" :class="{ white: day.whiteText }" v-if="index < day.items.length - 1"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="content-wrapper">
      <div class="image-list">
        <img 
          v-for="(img, index) in images" 
          :key="index" 
          :src="img" 
          class="list-item"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const images = [
  '/pic/images/未标题-1_01.jpg',
  '/pic/images/未标题-1_02.gif',
  '/pic/images/未标题-1_03.gif',
  '/pic/images/未标题-1_04.gif',
  '/pic/images/未标题-1_05.gif',
  '/pic/images/未标题-1_06.gif'
]

const URL_LINK = 'https://wxaurl.cn/WDb7jXTBqbc'

const scheduleData = ref([])

onMounted(async () => {
  try {
    const response = await fetch('/data/schedule.json')
    scheduleData.value = await response.json()
  } catch (error) {
    console.error('加载数据失败:', error)
  }
})

const handleItemClick = () => {
  window.location.href = URL_LINK
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  min-height: 100%;
}

#app {
  width: 100%;
  min-height: 100%;
}

.app-container {
  width: 100%;
  min-height: 200vh;
  background-image: url('/pic/背景图.png');
  background-size: 100% auto;
  background-position: top center;
  background-repeat: no-repeat;
  position: relative;
}

.header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 10;
}

.header-img {
  width: 70%;
  display: block;
  margin: 0 auto;
  padding-top: 140px;
}

.schedule-list {
  position: absolute;
  top: 540px;
  left: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.schedule-card {
  width: 100%;
  padding: 20px 14px 20px 18px;
  background-position: center;
  background-size: 100% 100%;
  background-repeat: no-repeat;
}

.date-text {
  font-size: 24px;
  font-weight: 800;
  color: #000;
  line-height: 32px;
  text-align: right;
  margin-bottom: 15px;
}

.schedule-items {
  display: flex;
  flex-direction: column;
}

.schedule-item {
  display: flex;
  flex-direction: column;
  padding: 8px 0;
  cursor: pointer;
}

.item-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 4px;
}

.time-block {
  display: flex;
  align-items: center;
  width: 100px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #000;
  margin-right: 5px;
  flex-shrink: 0;
}

.time-text {
  font-size: 12px;
  font-weight: 500;
  color: #000;
  white-space: nowrap;
}

.location {
  font-size: 12px;
  font-weight: 600;
  color: #000;
}

.activity {
  font-size: 14px;
  font-weight: 700;
  color: #000;
}

.signup {
  font-size: 12px;
  font-weight: 500;
  color: #076762;
  white-space: nowrap;
}

.divider {
  width: 100%;
  height: 1px;
  background: #000;
  margin-top: 6px;
}

.white {
  color: #fff !important;
}

.white.dot {
  background: #fff !important;
}

.white.divider {
  background: #fff !important;
}

.content-wrapper {
  width: 100%;
  background: transparent;
}

.image-list {
  width: 100%;
}

.list-item {
  width: 100%;
  display: block;
}
</style>
