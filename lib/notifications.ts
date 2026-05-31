'use client'

export async function enableBrowserNotifications() {
  if (!('Notification' in window)) {
    throw new Error('Notifications are not supported in this browser.')
  }
  const permission = await Notification.requestPermission()
  if (permission !== 'granted') {
    throw new Error('Notification permission was not granted.')
  }
  return true
}

export function sendBrowserNotification(title: string, body: string) {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(title, { body })
  }
}
