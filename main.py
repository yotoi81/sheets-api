from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, List, Optional
import gspread
from google.oauth2.service_account import Credentials
import os, json

app = FastAPI(title="Google Sheets API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "1IbeRjQTUVZqjsusAb0UrxaHtzaqvgw5sAX5HpsEL7qavV-kSMMzlT1W3")

def get_sheet(sheet_name: str = None):
    creds = Credentials.from_service_account_file(
        "/etc/secrets/credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    gc = gspread.authorize(creds)
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    if sheet_name:
        return spreadsheet.worksheet(sheet_name)
    return spreadsheet.sheet1

# Models
class WriteRequest(BaseModel):
    range: str           # เช่น "A1" หรือ "A1:C3"
    values: List[List[Any]]
    sheet_name: Optional[str] = None

class AppendRequest(BaseModel):
    values: List[List[Any]]
    sheet_name: Optional[str] = None

# ── GET all records ──────────────────────────────────────────
@app.get("/data")
def get_all_data(sheet_name: str = None):
    """ดึงข้อมูลทั้งหมดใน Sheet"""
    try:
        sheet = get_sheet(sheet_name)
        records = sheet.get_all_records()
        return {"status": "ok", "count": len(records), "data": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── GET specific range ───────────────────────────────────────
@app.get("/data/{range}")
def get_range(range: str, sheet_name: str = None):
    """ดึงข้อมูลตาม range เช่น A1:C10"""
    try:
        sheet = get_sheet(sheet_name)
        values = sheet.get(range)
        return {"status": "ok", "range": range, "values": values}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── POST write to range ──────────────────────────────────────
@app.post("/data/write")
def write_data(req: WriteRequest):
    """เขียนข้อมูลลงใน range ที่กำหนด"""
    try:
        sheet = get_sheet(req.sheet_name)
        sheet.update(req.range, req.values)
        return {"status": "ok", "message": f"เขียนข้อมูลไปที่ {req.range} แล้ว"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── POST append rows ─────────────────────────────────────────
@app.post("/data/append")
def append_data(req: AppendRequest):
    """เพิ่มแถวใหม่ต่อท้าย Sheet"""
    try:
        sheet = get_sheet(req.sheet_name)
        sheet.append_rows(req.values)
        return {"status": "ok", "message": f"เพิ่ม {len(req.values)} แถวแล้ว"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── DELETE clear range ───────────────────────────────────────
@app.delete("/data/{range}")
def clear_range(range: str, sheet_name: str = None):
    """ลบข้อมูลใน range ที่กำหนด"""
    try:
        sheet = get_sheet(sheet_name)
        sheet.batch_clear([range])
        return {"status": "ok", "message": f"ลบข้อมูลใน {range} แล้ว"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok", "message": "Google Sheets API is running 🚀"}
    @app.get("/debug")
def debug():
    import os
    try:
        with open("/etc/secrets/credentials.json") as f:
            data = json.load(f)
        return {
            "file_found": True,
            "client_email": data.get("client_email"),
            "private_key_start": data.get("private_key", "")[:30],
            "private_key_has_newline": "\\n" in data.get("private_key", "")
        }
    except Exception as e:
        return {"file_found": False, "error": str(e)}
