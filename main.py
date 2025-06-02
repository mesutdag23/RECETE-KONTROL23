from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

kullanici_listesi = []

class YeniUye(BaseModel):
    eczaci_kullanici_adi: str
    email: EmailStr
    medula_kullanici_adi: str
    medula_sifre: str
    sifre: str

class GirisVerisi(BaseModel):
    eczaci_kullanici_adi: str
    medula_kullanici_adi: str
    medula_sifre: str

@app.post("/uye-ol")
def uye_ol(uyelik: YeniUye):
    for kullanici in kullanici_listesi:
        if kullanici["eczaci_kullanici_adi"] == uyelik.eczaci_kullanici_adi:
            raise HTTPException(status_code=400, detail="Bu kullanıcı adı zaten alınmış.")
    kullanici_listesi.append(uyelik.dict())
    return {"mesaj": "Üyelik başarıyla oluşturuldu"}

@app.post("/giris")
def giris_kontrol(veri: GirisVerisi):
    for kullanici in kullanici_listesi:
        if (kullanici["eczaci_kullanici_adi"] == veri.eczaci_kullanici_adi and
            kullanici["medula_kullanici_adi"] == veri.medula_kullanici_adi and
            kullanici["medula_sifre"] == veri.medula_sifre):
            return {"mesaj": "Giriş başarılı"}
    raise HTTPException(status_code=401, detail="Giriş bilgileri hatalı")