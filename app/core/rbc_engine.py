import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from app.database.database import DatabaseConnection
from app.database import queries
from app.core.encoder_trainer import new_model, train_annoy_model, train_model


class AtendimentoRecommender:
    def __init__(self):
        self.db = DatabaseConnection()

    def recommend_local(self, tipo_gui, cod_con, cod_med, top_n=5):
        if not tipo_gui or not cod_con or not cod_med:
            raise ValueError("Campos obrigatórios 'tipogui', 'codcon' e 'codmed' não podem estar vazios.")

        query = queries.query_local(tipo_gui, cod_con, cod_med, meses=6)
        df = self.db.load_dataframeTeste(query)

        if df.empty:
            return []

        encoder, index, y = train_annoy_model(df, ["tipogui", "codcon", "codmed"], "codloc")

        input_df = pd.DataFrame([{
            "tipogui": tipo_gui,
            "codcon": cod_con,
            "codmed": cod_med
        }])

        input_encoded = encoder.transform(input_df).astype(np.float32)
        input_encoded = normalize(input_encoded, axis=1)

        indices, distances = index.get_nns_by_vector(input_encoded[0], top_n, include_distances=True)
        top_series = y.iloc[indices].value_counts()

        recomendacoes = [
            {"code": str(code), "description": ""}
            for code in top_series.index[:5]
        ] if not top_series.empty else []

        return recomendacoes

    def recommend_acomoda(self, tipo_gui, cod_con, cod_loc, cod_med, top_n=5):
        if not tipo_gui or not cod_con or not cod_loc or not cod_med:
            raise ValueError("Campos obrigatórios 'tipogui', 'codcon', 'codloc' e 'codmed' não podem estar vazios.")

        query = queries.query_acomodacao(tipo_gui, cod_con, cod_loc, cod_med)
        df = self.db.load_dataframeTeste(query)

        if df.empty:
            return []

        encoder, index, y = train_model(df, ["tipogui", "codcon", "codloc", "codmed"], "acomoda")

        input_df = pd.DataFrame([{
            "tipogui": tipo_gui,
            "codcon": cod_con,
            "codloc": cod_loc,
            "codmed": cod_med
        }])

        input_encoded = encoder.transform(input_df).toarray().astype(np.float32)
        input_encoded = normalize(input_encoded, axis=1)

        distances, indices = index.search(input_encoded, top_n)
        top_series = y.iloc[indices[0]].value_counts()

        recomendacoes = [
            {"code": str(code), "description": ""}
            for code in top_series.index[:5]
        ] if not top_series.empty else []

        return recomendacoes

    def recommend_proced(self, tipo_gui, cod_con, cod_loc, acomodacao, cod_med, top_n=5):
        if not tipo_gui or not cod_con or not cod_loc or not acomodacao or not cod_med:
            raise ValueError("Campos obrigatórios 'tipogui', 'codcon', 'codloc', 'acomoda' e 'codmed' não podem estar vazios.")

        query_all = queries.query_procedimentos(tipo_gui, cod_con, cod_loc, acomodacao, cod_med, last_6_months=False)
        df_all = self.db.load_dataframeTeste(query_all)

        if df_all.empty:
            return []

        encoder_all, index_all, y_all = train_model(df_all, ["tipogui", "codcon", "codloc", "acomoda", "codmed"], "codpro")

        input_df = pd.DataFrame([{
            "tipogui": tipo_gui,
            "codcon": cod_con,
            "codloc": cod_loc,
            "acomoda": acomodacao,
            "codmed": cod_med
        }])

        input_encoded = encoder_all.transform(input_df).toarray().astype(np.float32)
        input_encoded = normalize(input_encoded, axis=1)

        distances_all, indices_all = index_all.search(input_encoded, top_n)
        top_series_all = y_all.iloc[indices_all[0]].value_counts()

        query_6mo = queries.query_procedimentos(tipo_gui, cod_con, cod_loc, acomodacao, cod_med, last_6_months=True)
        df_6mo = self.db.load_dataframeTeste(query_6mo)

        if not df_6mo.empty:
            encoder_6mo, index_6mo, y_6mo = train_model(df_6mo, ["tipogui", "codcon", "codloc", "acomoda", "codmed"], "codpro")
            input_encoded_6mo = encoder_6mo.transform(input_df).toarray().astype(np.float32)
            input_encoded_6mo = normalize(input_encoded_6mo, axis=1)

            distances_6mo, indices_6mo = index_6mo.search(input_encoded_6mo, top_n)
            top_series_6mo = y_6mo.iloc[indices_6mo[0]].value_counts()
            recomendacoes_6mo = top_series_6mo.index[:5].tolist() if not top_series_6mo.empty else []
        else:
            recomendacoes_6mo = []

        recomendacoes = [
            {"code": str(code), "description": ""}
            for code in top_series_all.index[:5]
        ] if not top_series_all.empty else []

        return recomendacoes
