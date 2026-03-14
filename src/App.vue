<template>
  <div class="app-container">
    <div class="header">
      <img src="/pic/logo.png" class="header-img" />
    </div>
    <img 
      src="/pic/work_shop.png" 
      class="work-shop-img"
      :style="{ top: scheduleListTop + 'px' }"
      :ref="workShopRef"
      @load="onWorkShopLoad"
      @click="handleWorkShopClick"
    />
    <div class="schedule-list" :style="{ top: scheduleListTop + workShopTop + 'px' }">
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
            @click="handleSignup(item)"
          >
            <div class="item-main">
              <div class="item-row">
                <div class="time-block">
                  <div class="dot" :class="{ white: day.whiteText }"></div>
                  <span class="time-text" :class="{ white: day.whiteText }">{{ item.time }}</span>
                </div>
                <span class="location" :class="{ white: day.whiteText }">{{ item.location }}</span>
              </div>
              <div class="item-row activity-row">
                <span class="activity" :class="{ white: day.whiteText }" v-html="item.activity"></span>
                <span 
                  class="signup" 
                  :class="{ white: day.whiteText }"
                >{{ item.signup }}</span>
              </div>
            </div>
            <div class="host-section" v-if="item.host">
              <span class="host-name" :class="{ white: day.whiteText }">{{ item.host.name }}</span>
              <div class="host-divider" :class="{ white: day.whiteText }"></div>
              <span class="host-title" :class="{ white: day.whiteText }" v-html="item.host.title.replace(/\n/g, '<br>')"></span>
            </div>
            <div class="guests-section" v-if="item.guests && item.guests.length > 0">
              <div class="guest" v-for="(guest, gIndex) in item.guests" :key="gIndex">
                <span class="guest-name" :class="{ white: day.whiteText }">{{ guest.name }}</span>
                <div class="guest-divider" :class="{ white: day.whiteText }"></div>
                <span class="guest-title" :class="{ white: day.whiteText }" v-html="guest.title.replace(/\n/g, '<br>')"></span>
              </div>
            </div>
            <div class="divider" :class="{ white: day.whiteText }" v-if="index < day.items.length - 1"></div>
          </div>
        </div>
      </div>
      <img src="/pic/cooperative_partner.png" class="cooperative-partner" />
    </div>
    
    <div class="content-wrapper">
      <div class="image-list">
        <img 
          v-for="(img, index) in images" 
          :key="index" 
          :src="img" 
          class="list-item"
          :ref="el => { if (index === 0) firstImageRef = el }"
          @load="onFirstImageLoad"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import jweixin from 'weixin-js-sdk'

const images = [
  '/pic/images/bg_1.jpg',
  '/pic/images/bg_2.jpg',
  '/pic/images/bg_3.jpg',
  '/pic/images/bg_4.jpg',
  '/pic/images/bg_5.jpg',
  '/pic/images/bg_6.jpg',
  '/pic/images/bg_7.jpg',
  '/pic/images/bg_8.jpg',
  '/pic/images/bg_9.jpg',
  '/pic/images/bg_10.jpg',
]

const URL_LINK = 'https://wxaurl.cn/ThyeBBtTz6q'
const APP_ID = 'wx68aec81c081a8e6c'
const DEFAULT_PATH = 'subpackages/main/webview/index.html?activityId=0bcf4dac0c000000&circleId=1&title=activityDetail&fromShare=1'

const isWeChatBrowser = ref(false)
const isMiniProgram = ref(false)
const firstImageRef = ref(null)
const workShopRef = ref(null)
const workShopTop = ref(140)
const scheduleListTop = ref(540)

const onFirstImageLoad = () => {
  if (firstImageRef.value) {
    const imageHeight = firstImageRef.value.clientHeight
    scheduleListTop.value = imageHeight
  }
}

const onWorkShopLoad = () => {
  if (workShopRef.value) {
    workShopTop.value = workShopRef.value.clientHeight + 15
  }
}

const isWeChat = () => {
  const userAgent = navigator.userAgent.toLowerCase()
  return userAgent.indexOf('micromessenger') > -1
}

const isInMiniProgram = () => {
  return window.__wxjs_environment === 'miniprogram' || navigator.userAgent.includes('miniProgram')
}

const handleSignup = (item) => {
  const activityId = item.activityId || '0bcf4dac0c000000'
  const circleId = item.circleId || '1'
  
  window.location.href = item.signupUrl || URL_LINK
}

const handleWorkShopClick = () => {
  window.location.href = URL_LINK
}

const scheduleData = ref([])

onMounted(async () => {
  isWeChatBrowser.value = isWeChat()
  isMiniProgram.value = isInMiniProgram()
  
  if (firstImageRef.value) {
    const imageHeight = firstImageRef.value.clientHeight
    if (imageHeight > 0) {
      scheduleListTop.value = imageHeight
    }
  }
  
  try {
    const response = await fetch('/data/schedule.json')
    scheduleData.value = await response.json()
  } catch (error) {
    console.error('加载数据失败:', error)
  }
})
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
  background-color: transparent;
}

#app {
  width: 100%;
  min-height: 100%;
  background-color: transparent;
}

.app-container {
  width: 100%;
  min-height: 200vh;
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
  width: 90%;
  display: block;
  margin: 0 auto;
  padding-top: 140px;
}

.work-shop-img {
  position: absolute;
  left: 10px;
  right: 0;
  width: 97.3%;
  z-index: 100;
}

.schedule-list {
  position: absolute;
  left: 10px;
  right: 0px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  z-index: 10;
  transition: top 0.3s ease;
}

.schedule-card {
  width: 100%;
  padding: 20px 14px 20px 18px;
  background-position: center;
  background-size: 100% 100%;
  background-repeat: no-repeat;
}

.date-text {
  font-size: 26px;
  font-weight: 900;
  color: #000;
  line-height: 30px;
  text-align: right;
  margin-bottom: 10px;
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

.item-main {
  display: flex;
  flex-direction: column;
}

.activity-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-top: 3px;
}

.guests-section {
  margin-top: 8px;
  margin-left: 11px;
  display: flex;
  flex-direction: column;
}

.guest {
  display: flex;
  align-items: flex-start;
  margin-bottom: 4px;
}

.guest-name {
  font-size: 14px;
  font-weight: 700;
  color: #000;
  min-width: 80px;
}

.guest-divider {
  width: 13px;
  height: 1px;
  background: #000;
  margin-top: 6px;
  transform: rotate(90deg);
  margin-left: 5px;
  margin-right: 5px;
}

.guest-title {
  font-size: 14px;
  font-weight: 500;
  color: #000;
  line-height: 16px;
}

.host-section {
  margin-top: 8px;
  margin-left: 11px;
  display: flex;
  align-items: flex-start;
}

.host-name {
  font-size: 14px;
  font-weight: 700;
  color: #000;
}

.host-divider {
  width: 13px;
  height: 1px;
  background: #000;
  transform: rotate(90deg);
  margin: 8px 5px 0 5px;
}

.host-title {
  font-size: 14px;
  font-weight: 500;
  color: #000;
  line-height: 16px;
}

.item-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 2px;
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
  font-size: 14px;
  font-weight: 500;
  color: #000;
  white-space: nowrap;
}

.location {
  font-size: 14px;
  font-weight: 500;
  color: #000;
}

.activity {
  font-size: 16px;
  font-weight: 700;
  margin-right: 5px;
  color: #000;
}

.signup {
  font-size: 14px;
  font-weight: 500;
  color: #058c8a;
  white-space: nowrap;
}

.signup-link {
  color: inherit;
  text-decoration: none;
}

.weapp-btn {
  color: inherit;
  font-size: inherit;
  font-weight: inherit;
}

.btn-text {
  color: inherit;
  font-size: inherit;
  font-weight: inherit;
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

.white.guest-divider,
.white.host-divider {
  background: #fff !important;
}

.white.weapp-btn,
.white .btn-text {
  color: #fff !important;
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

.cooperative-partner {
  width: 90%;
  height: auto;
  display: block;
  margin: 0 auto;
  margin-left: 10px;
  padding-top: 2px;
}
</style>
