const token = process.env.LINE_CHANNEL_ACCESS_TOKEN;

if (!token) {
  console.error('Missing LINE_CHANNEL_ACCESS_TOKEN. Add it in GitHub Settings → Secrets and variables → Actions.');
  process.exit(1);
}

const richMenu = {
  size: { width: 2500, height: 843 },
  selected: true,
  name: 'TinyTangyuan Rich Menu A',
  chatBarText: '選單',
  areas: [
    {
      bounds: { x: 0, y: 0, width: 833, height: 843 },
      action: { type: 'message', text: '首頁' }
    },
    {
      bounds: { x: 833, y: 0, width: 834, height: 843 },
      action: { type: 'message', text: '功能' }
    },
    {
      bounds: { x: 1667, y: 0, width: 833, height: 843 },
      action: { type: 'message', text: '更多' }
    }
  ]
};

const response = await fetch('https://api.line.me/v2/bot/richmenu', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(richMenu)
});

const text = await response.text();

if (!response.ok) {
  console.error(`LINE API error ${response.status}: ${text}`);
  process.exit(1);
}

const result = JSON.parse(text);
console.log(`Rich Menu A created successfully.`);
console.log(`richMenuId=${result.richMenuId}`);
