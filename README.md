# Google Sheets API Server

## Deploy บน Render (ฟรี)

### ขั้นตอน
1. Push โฟลเดอร์นี้ขึ้น GitHub
2. ไปที่ render.com → New → Web Service
3. เชื่อม GitHub repo
4. ใส่ Environment Variables:
   - `GOOGLE_CREDENTIALS` = วาง JSON ทั้งก้อนจาก Service Account key
   - `SPREADSHEET_ID` = ID ของ Sheet คุณ
5. Deploy ✅

### เตรียม Google Credentials
1. ไป https://console.cloud.google.com
2. สร้างโปรเจกต์ → เปิด Google Sheets API
3. IAM → Service Accounts → สร้างใหม่ → ดาวน์โหลด JSON
4. แชร์ Sheet ให้ email ของ Service Account (Editor)

## API Endpoints

| Method | Path | คำอธิบาย |
|--------|------|----------|
| GET | /data | ดึงข้อมูลทั้งหมด |
| GET | /data/{range} | ดึงข้อมูลตาม range เช่น A1:C10 |
| POST | /data/write | เขียนข้อมูลลง range |
| POST | /data/append | เพิ่มแถวใหม่ |
| DELETE | /data/{range} | ลบข้อมูลใน range |

## ตัวอย่าง Request

### ดึงข้อมูล
```
GET https://your-app.onrender.com/data
```

### เขียนข้อมูล
```json
POST /data/write
{
  "range": "A1",
  "values": [["ชื่อ", "อายุ"], ["สมชาย", "30"]]
}
```

### เพิ่มแถว
```json
POST /data/append
{
  "values": [["สมหญิง", "25"]]
}
```
