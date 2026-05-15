"""
Global Demografiya Tahlili - Analyzer moduli
============================================
Barcha tahlil funksiyalari shu yerda
"""

import pandas as pd
import numpy as np
import os


class DemographyAnalyzer:
    """Demografik ma'lumotlarni tahlil qiluvchi asosiy klass"""

    USTUNLAR_UZ = {
        'country': 'Davlat',
        'country_code': 'Kod',
        'continent': 'Qita',
        'year': 'Yil',
        'population': 'Aholi',
        'gdp_per_capita': 'AHM (USD)',
        'life_expectancy': 'Umr (yil)',
        'birth_rate': "Tug'ilish (‰)",
        'death_rate': "O'lim (‰)",
        'urban_population_pct': 'Shahar aholisi (%)',
        'fertility_rate': 'Fertillik',
        'median_age': "O'rtacha yosh",
        'literacy_rate': 'Savodxonlik (%)'
    }

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df = self._yuklash()

    def _yuklash(self) -> pd.DataFrame:
        """CSV ma'lumotlarini yuklash"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Ma'lumotlar fayli topilmadi: {self.data_path}")
        df = pd.read_csv(self.data_path)
        return df

    def _raqam(self, qiymat):
        """NaN qiymatlarni None ga aylantirish"""
        if pd.isna(qiymat):
            return None
        if isinstance(qiymat, (np.integer,)):
            return int(qiymat)
        if isinstance(qiymat, (np.floating,)):
            return round(float(qiymat), 2)
        return qiymat

    def barcha_davlatlar(self) -> list:
        """Barcha davlatlar ro'yxati"""
        return [
            {
                "davlat": row['country'],
                "kod": row['country_code'],
                "qita": row['continent'],
                "aholi": int(row['population'])
            }
            for _, row in self.df.iterrows()
        ]

    def umumiy_statistika(self) -> dict:
        """Global umumiy statistika"""
        return {
            "jami_davlatlar": len(self.df),
            "jami_aholi": int(self.df['population'].sum()),
            "global_urtacha_umr": round(float(self.df['life_expectancy'].mean()), 1),
            "global_urtacha_gdp": round(float(self.df['gdp_per_capita'].mean()), 0),
            "global_urtacha_tug_ilish": round(float(self.df['birth_rate'].mean()), 1),
            "global_urtacha_fertillik": round(float(self.df['fertility_rate'].mean()), 2),
            "eng_kop_aholi": {
                "davlat": self.df.loc[self.df['population'].idxmax(), 'country'],
                "aholi": int(self.df['population'].max())
            },
            "eng_kam_aholi": {
                "davlat": self.df.loc[self.df['population'].idxmin(), 'country'],
                "aholi": int(self.df['population'].min())
            },
            "eng_yuqori_umr": {
                "davlat": self.df.loc[self.df['life_expectancy'].idxmax(), 'country'],
                "yil": float(self.df['life_expectancy'].max())
            },
            "eng_past_umr": {
                "davlat": self.df.loc[self.df['life_expectancy'].idxmin(), 'country'],
                "yil": float(self.df['life_expectancy'].min())
            },
            "eng_yuqori_gdp": {
                "davlat": self.df.loc[self.df['gdp_per_capita'].idxmax(), 'country'],
                "usd": float(self.df['gdp_per_capita'].max())
            },
            "qitalar": self.df['continent'].nunique(),
            "shaharlik_urtacha": round(float(self.df['urban_population_pct'].mean()), 1),
            "urtacha_yosh": round(float(self.df['median_age'].mean()), 1)
        }

    def davlat_malumoti(self, kod: str) -> dict | None:
        """Bitta davlat haqida batafsil ma'lumot"""
        qator = self.df[self.df['country_code'] == kod]
        if qator.empty:
            # Nom bo'yicha ham qidirish
            qator = self.df[self.df['country'].str.upper() == kod]
        if qator.empty:
            return None

        r = qator.iloc[0]

        # Reyting hisoblash (aholi bo'yicha)
        aholi_reyting = int((self.df['population'] > r['population']).sum()) + 1
        gdp_reyting = int((self.df['gdp_per_capita'] > r['gdp_per_capita']).sum()) + 1
        umr_reyting = int((self.df['life_expectancy'] > r['life_expectancy']).sum()) + 1

        return {
            "davlat": r['country'],
            "kod": r['country_code'],
            "qita": r['continent'],
            "yil": int(r['year']),
            "aholi": int(r['population']),
            "aholi_reyting": f"{aholi_reyting}/{len(self.df)}",
            "gdp_per_capita": float(r['gdp_per_capita']),
            "gdp_reyting": f"{gdp_reyting}/{len(self.df)}",
            "umr_davomiyligi": float(r['life_expectancy']),
            "umr_reyting": f"{umr_reyting}/{len(self.df)}",
            "tug_ilish_darajasi": float(r['birth_rate']),
            "olim_darajasi": float(r['death_rate']),
            "shahar_aholi_ulushi": float(r['urban_population_pct']),
            "fertillik_darajasi": float(r['fertility_rate']),
            "urtacha_yosh": float(r['median_age']),
            "savodxonlik": float(r['literacy_rate']),
            "tavsif": self._davlat_tavsifi(r)
        }

    def _davlat_tavsifi(self, r) -> str:
        """Davlat uchun qisqa demografik tavsif"""
        tavsiflar = []

        if r['life_expectancy'] >= 82:
            tavsiflar.append("yuqori umr davomiyligi")
        elif r['life_expectancy'] < 65:
            tavsiflar.append("past umr davomiyligi")

        if r['gdp_per_capita'] >= 30000:
            tavsiflar.append("yuqori daromadli")
        elif r['gdp_per_capita'] < 2000:
            tavsiflar.append("past daromadli")
        else:
            tavsiflar.append("o'rta daromadli")

        if r['fertility_rate'] >= 4:
            tavsiflar.append("yuqori tug'ilish")
        elif r['fertility_rate'] < 1.5:
            tavsiflar.append("past tug'ilish")

        if r['urban_population_pct'] >= 85:
            tavsiflar.append("urbanizatsiyalashgan")

        return ", ".join(tavsiflar).capitalize() + " davlat"

    def qitalar_statistikasi(self) -> list:
        """Qitalar bo'yicha statistika"""
        natija = []
        for qita, guruh in self.df.groupby('continent'):
            natija.append({
                "qita": qita,
                "davlatlar_soni": len(guruh),
                "jami_aholi": int(guruh['population'].sum()),
                "urtacha_umr": round(float(guruh['life_expectancy'].mean()), 1),
                "urtacha_gdp": round(float(guruh['gdp_per_capita'].mean()), 0),
                "urtacha_fertillik": round(float(guruh['fertility_rate'].mean()), 2),
                "urtacha_shaharlik": round(float(guruh['urban_population_pct'].mean()), 1),
                "urtacha_yosh": round(float(guruh['median_age'].mean()), 1),
                "eng_kop_aholi_davlat": guruh.loc[guruh['population'].idxmax(), 'country'],
                "eng_yuqori_gdp_davlat": guruh.loc[guruh['gdp_per_capita'].idxmax(), 'country']
            })
        return sorted(natija, key=lambda x: x['jami_aholi'], reverse=True)

    def top_davlatlar(self, ustun: str, n: int = 10, kamayuvchi: bool = True) -> list:
        """Biror ko'rsatkich bo'yicha top davlatlar"""
        tartiblangan = self.df.sort_values(ustun, ascending=not kamayuvchi).head(n)
        natija = []
        for i, (_, r) in enumerate(tartiblangan.iterrows(), 1):
            natija.append({
                "o'rin": i,
                "davlat": r['country'],
                "kod": r['country_code'],
                "qita": r['continent'],
                ustun: self._raqam(r[ustun]),
                "aholi": int(r['population'])
            })
        return natija

    def davlatlarni_taqqoslash(self, kodlar: list) -> dict:
        """Bir necha davlatni taqqoslash"""
        natija = []
        topilmagan = []
        for kod in kodlar:
            qator = self.df[self.df['country_code'] == kod]
            if qator.empty:
                topilmagan.append(kod)
                continue
            r = qator.iloc[0]
            natija.append({
                "davlat": r['country'],
                "kod": r['country_code'],
                "qita": r['continent'],
                "aholi": int(r['population']),
                "gdp_per_capita": float(r['gdp_per_capita']),
                "umr_davomiyligi": float(r['life_expectancy']),
                "tug_ilish": float(r['birth_rate']),
                "olim": float(r['death_rate']),
                "shaharlik": float(r['urban_population_pct']),
                "fertillik": float(r['fertility_rate']),
                "urtacha_yosh": float(r['median_age']),
                "savodxonlik": float(r['literacy_rate'])
            })
        return {
            "taqqoslash": natija,
            "topilmagan": topilmagan,
            "eng_kop_aholi": max(natija, key=lambda x: x['aholi'])['davlat'] if natija else None,
            "eng_yuqori_gdp": max(natija, key=lambda x: x['gdp_per_capita'])['davlat'] if natija else None,
            "eng_yuqori_umr": max(natija, key=lambda x: x['umr_davomiyligi'])['davlat'] if natija else None,
        }

    def aholi_turmush_tahlili(self, qita: str = None) -> dict:
        """Aholi va turmush sifati korrelyatsion tahlili"""
        df = self.df if qita is None else self.df[self.df['continent'] == qita]

        scatter_data = []
        for _, r in df.iterrows():
            scatter_data.append({
                "davlat": r['country'],
                "kod": r['country_code'],
                "qita": r['continent'],
                "gdp": float(r['gdp_per_capita']),
                "umr": float(r['life_expectancy']),
                "aholi": int(r['population']),
                "fertillik": float(r['fertility_rate'])
            })

        return {
            "qita": qita or "Barchasi",
            "davlatlar_soni": len(df),
            "scatter_data": scatter_data,
            "gdp_umr_korrelyatsiya": round(float(df['gdp_per_capita'].corr(df['life_expectancy'])), 3),
            "gdp_fertillik_korrelyatsiya": round(float(df['gdp_per_capita'].corr(df['fertility_rate'])), 3)
        }

    def qidirish(self, qidiruv: str) -> list:
        """Davlat nomi yoki kodi bo'yicha qidirish"""
        q = qidiruv.lower()
        mask = (
            self.df['country'].str.lower().str.contains(q, na=False) |
            self.df['country_code'].str.lower().str.contains(q, na=False) |
            self.df['continent'].str.lower().str.contains(q, na=False)
        )
        natija = []
        for _, r in self.df[mask].iterrows():
            natija.append({
                "davlat": r['country'],
                "kod": r['country_code'],
                "qita": r['continent'],
                "aholi": int(r['population']),
                "gdp_per_capita": float(r['gdp_per_capita']),
                "umr_davomiyligi": float(r['life_expectancy'])
            })
        return natija

    def demografik_tasnif(self) -> dict:
        """Demografik guruhlar bo'yicha tasnif"""

        def gdp_turi(gdp):
            if gdp >= 30000: return "Yuqori daromadli"
            elif gdp >= 10000: return "Yuqori-o'rta daromadli"
            elif gdp >= 3000: return "Quyi-o'rta daromadli"
            else: return "Past daromadli"

        def umr_turi(umr):
            if umr >= 80: return "Juda yuqori (80+)"
            elif umr >= 75: return "Yuqori (75-80)"
            elif umr >= 70: return "O'rtacha (70-75)"
            else: return "Past (<70)"

        def fertillik_turi(f):
            if f >= 4: return "Yuqori (4+)"
            elif f >= 2.1: return "O'rtacha (2.1-4)"
            elif f >= 1.5: return "Past (1.5-2.1)"
            else: return "Juda past (<1.5)"

        gdp_guruh = self.df.groupby(self.df['gdp_per_capita'].apply(gdp_turi)).agg(
            soni=('country', 'count'),
            jami_aholi=('population', 'sum'),
            urtacha_umr=('life_expectancy', 'mean')
        ).round(1).reset_index()

        umr_guruh = self.df.groupby(self.df['life_expectancy'].apply(umr_turi)).agg(
            soni=('country', 'count'),
            jami_aholi=('population', 'sum')
        ).reset_index()

        fert_guruh = self.df.groupby(self.df['fertility_rate'].apply(fertillik_turi)).agg(
            soni=('country', 'count'),
            jami_aholi=('population', 'sum')
        ).reset_index()

        return {
            "gdp_guruhlar": gdp_guruh.to_dict('records'),
            "umr_guruhlar": umr_guruh.to_dict('records'),
            "fertillik_guruhlar": fert_guruh.to_dict('records')
        }

    def korrelatsiya_tahlili(self) -> dict:
        """Ko'rsatkichlar o'rtasidagi korrelyatsiya matritsasi"""
        ustunlar = ['gdp_per_capita', 'life_expectancy', 'birth_rate',
                    'death_rate', 'fertility_rate', 'median_age',
                    'urban_population_pct', 'literacy_rate']

        corr_matrix = self.df[ustunlar].corr().round(3)

        # Eng kuchli korrelyatsiyalar
        kuchli = []
        for i in range(len(ustunlar)):
            for j in range(i + 1, len(ustunlar)):
                val = corr_matrix.iloc[i, j]
                if abs(val) >= 0.6:
                    kuchli.append({
                        "o'zgaruvchi_1": ustunlar[i],
                        "o'zgaruvchi_2": ustunlar[j],
                        "korrelyatsiya": round(float(val), 3),
                        "kuch": "Kuchli musbat" if val > 0 else "Kuchli manfiy"
                    })

        return {
            "matritsa": corr_matrix.to_dict(),
            "ustunlar": ustunlar,
            "kuchli_korrelyatsiyalar": sorted(kuchli, key=lambda x: abs(x['korrelyatsiya']), reverse=True)
        }
