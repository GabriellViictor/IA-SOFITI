def query_local(tipo_gui, cod_con, cod_med, meses=6):
    return f"""
        SELECT "tipogui", "codcon", "codmed", "codloc"
        FROM public."procedimentos"
        WHERE "tipogui" = '{tipo_gui}'
          AND "codcon" = '{cod_con}'
          AND "codmed" = '{cod_med}'
    """

def query_acomodacao(tipo_gui, cod_con, cod_loc, cod_med):
    return f'''
        SELECT "tipogui", "codcon", "codloc", "acomoda", "codmed"
        FROM public."procedimentos"
        WHERE "tipogui" = '{tipo_gui}' 
        AND "codcon" = '{cod_con}' 
        AND "codloc" = '{cod_loc}' 
        AND "codmed" = '{cod_med}'
    '''

def query_procedimentos(tipo_gui, cod_con, cod_loc, acomodacao, cod_med, last_6_months=False):
    date_filter = '''
        AND TO_DATE("dtini", 'YYYYMMDD') >= (CURRENT_DATE - INTERVAL '24 MONTH')
    ''' if last_6_months else ""
    
    return f'''
        SELECT "tipogui", "codcon", "codloc", "acomoda", "codpro", "codmed", "dtini"
        FROM public."procedimentos"
        WHERE "tipogui" = '{tipo_gui}' 
          AND "codcon" = '{cod_con}' 
          AND "codmed" = '{cod_med}'
          AND "codloc" = '{cod_loc}' 
          AND "acomoda" = '{acomodacao}'
          {date_filter}
    '''



def query_CodLoc(cod_loc):
    return f'''
        SELECT "z2_nomloc"
        FROM public."locais"
        WHERE "z2_codloc" = '{cod_loc}' 
    '''
