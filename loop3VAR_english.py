import pandas as pd
import numpy as np
import sys as s

period_ag=input("TIME RANGE: ")
period_ag_int=int(period_ag)*60
frecuencys=[]
frecuencys.append(str(period_ag_int)+'s')
num_periods_back=input("BACK TIME: ")
periods_back=[]
periods_back=[i for i in range(int(num_periods_back))]
max_period=int(num_periods_back)-1
combinations=4
campos=[]
campos_aux=[]
desc=["2V2E","2V","V","VE"]
campos_print=[]
for frecuency in frecuencys:
	dfv1=pd.read_csv('S:\proyecto2\csv\VARIABLE1.csv', parse_dates=['FECHA'])
	dfv2=pd.read_csv('S:\proyecto2\csv\VARIABLE2.csv', parse_dates=['FECHA'])
	#dfv3=pd.read_csv('S:\proyecto2\csv\VARIABLE3.csv', parse_dates=['FECHA'])
	df2v1=dfv1.groupby(['VARIABLE1',pd.Grouper(key='FECHA',freq=frecuency)])['VALOR'].agg(['mean','count','std'])
	df2v2=dfv2.groupby(['VARIABLE2',pd.Grouper(key='FECHA',freq=frecuency)])['VALOR'].agg(['mean','count','std'])
	#df2v3=dfv3.groupby(['VARIABLE3',pd.Grouper(key='FECHA',freq=frecuency)])['VALOR'].agg(['mean','count','std'])
	df2v1['ERROR']=(df2v1['std']/(np.sqrt(df2v1['count'])))
	df2v2['ERROR']=(df2v2['std']/(np.sqrt(df2v2['count'])))
	#df2v3['ERROR']=(df2v3['std']/(np.sqrt(df2v3['count'])))
	df2v1=df2v1.drop('count',1)
	df2v2=df2v2.drop('count',1)
	#df2v3=df2v3.drop('count',1)
	df2v1=df2v1.drop('std',1)
	df2v2=df2v2.drop('std',1)
	#df2v2=df2v3.drop('std',1)
	df2v1.rename(columns={'mean':'MEDIA'},inplace=True)
	df2v2.rename(columns={'mean':'MEDIA'},inplace=True)
	#df2v3.rename(columns={'mean':'MEDIA'},inplace=True)
	df2v1=df2v1.reset_index()
	df2v2=df2v2.reset_index()
	#df2v3=df2v3.reset_index()
	df2v1['indice']=df2v1.index
	df2v2['indice']=df2v2.index
	#df2v3['indice']=df2v3.index
	cols=['indice','FECHA','MEDIA','ERROR']
	df2v1=df2v1[cols]
	df2v2=df2v2[cols]
	#df2v3=df2v2[cols]
	#df2v1.to_csv('S:\proyecto2\csv\SCENES\V1'+frecuency+'.csv',index=False)
	#df2v2.to_csv('S:\proyecto2\csv\SCENES\V2'+frecuency+'.csv',index=False)
	stage=[i for i in periods_back]
	tmp_dfv1=[j for j in periods_back]
	tmp_dfv2=[k for k in periods_back]
	#tmp_dfv3=[h for h in periods_back]
	frecuency_int=int(frecuency.replace("s",""))
	frecuency_int=frecuency_int/60
	frec_scene=str(frecuency_int)+"min"
	
	
	for period_back in periods_back:
		cont=int(num_periods_back)-period_back
		tmp_dfv1[period_back]=df2v1
		tmp_dfv2[period_back]=df2v2	
		#tmp_dfv3[period_back]=df2v3
		stage[period_back]=pd.merge(df2v2,df2v1, on='indice', how='left')		
		tmp_dfv1[period_back]=tmp_dfv1[period_back][tmp_dfv1[period_back].indice>period_back]
		tmp_dfv2[period_back]=tmp_dfv2[period_back][tmp_dfv2[period_back].indice>period_back]
		#tmp_dfv3[period_back]=tmp_dfv3[period_back][tmp_dfv3[period_back].indice>period_back]
		tmp_dfv1[period_back]=tmp_dfv1[period_back].reset_index()
		tmp_dfv2[period_back]=tmp_dfv2[period_back].reset_index()
		#tmp_dfv3[period_back]=tmp_dfv3[period_back].reset_index()
		tmp_dfv1[period_back]['indice']=tmp_dfv1[period_back].index
		tmp_dfv2[period_back]['indice']=tmp_dfv2[period_back].index
		#tmp_dfv3[period_back]['indice']=tmp_dfv3[period_back].index
		cols=['indice','FECHA','MEDIA','ERROR']
		tmp_dfv1[period_back]=tmp_dfv1[period_back][cols]
		tmp_dfv2[period_back]=tmp_dfv2[period_back][cols]
		#tmp_dfv3[period_back]=tmp_dfv3[period_back][cols]
		
		#tmp_dfv1[period_back].rename(columns={'FECHA':'V1_FECHA-'+str(cont),'MEDIA':'V1_MEDIA-'+str(cont),'ERROR':'V1_ERROR-'+str(cont)},inplace=True)
		#tmp_dfv2[period_back].rename(columns={'FECHA':'V2_FECHA-'+str(cont),'MEDIA':'V2_MEDIA-'+str(cont),'ERROR':'V2_ERROR-'+str(cont)},inplace=True)
		#tmp_dfv1[period_back].to_csv('S:\proyecto2\csv\SCENES\V1'+frecuency+'-'+str(period_back)+'.csv',index=False)
		#tmp_dfv2[period_back].to_csv('S:\proyecto2\csv\SCENES\V2'+frecuency+'-'+str(period_back)+'.csv',index=False)				
	for period_back in reversed(periods_back):
		if period_back==int(num_periods_back)-1:
			#stage[period_back]=pd.merge(stage[period_back],tmp_dfv1[max_period-period_back], on='indice', how='left', suffixes=['_l', '_r'])
			stage[period_back]=pd.merge(tmp_dfv1[max_period-period_back],stage[period_back], on='indice', how='left', suffixes=['_l', '_r'])
			stage[period_back].rename(columns={'FECHA_x':'V2_FECHA-1','MEDIA_x':'V2_MEDIA-1','ERROR_x':'V2_ERROR-1'},inplace=True)
			stage[period_back].rename(columns={'FECHA_y':'V1_FECHA-1','MEDIA_y':'V1_MEDIA-1','ERROR_y':'V1_ERROR-1'},inplace=True)
			for comb in range(combinations):
				#print(comb)	
				if comb==0:
					campos=[i for i in range(len(stage[period_back].columns)-1)]
					campos.pop(0)
					for i in range (1,len(campos)-2,3):
						campos.remove(i)					
					print (campos)
					campos_print=campos[:]
					campos_print.insert(0,campos[-2])
					campos_print.pop(-2)
					stage2=stage[period_back].iloc[:,pd.eval(campos_print)]
					stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
				if comb==1:
					for i in range (3,campos[-1]-1,3):
						campos.remove(i)
						campos_print=campos[:]
						campos_print.insert(0,campos[-2])
						campos_print.pop(-2)
						stage2=stage[period_back].iloc[:,pd.eval(campos_print)]
						stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print (campos)
				if comb==2:
					campos.pop(0)
					campos_print=campos[:]
					campos_print.insert(0,campos[-2])
					campos_print.pop(-2)
					stage2=stage[period_back].iloc[:,pd.eval(campos_print)]
					stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print (campos)
				if comb==3:
					campos_aux.append(campos[0])
					campos_aux.append(campos[0]+1)
					campos.pop(0)	
					campos.insert(0,campos_aux[1])
					campos.insert(0,campos_aux[0])
					campos_print=campos[:]
					campos_print.insert(0,campos[-2])
					campos_print.pop(-2)
					stage2=stage[period_back].iloc[:,pd.eval(campos_print)]
					stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print(campos)						
			#stage[period_back].to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'.csv',index=False)		
			#print(len(stage[period_back].columns))
			#stage[period_back]=pd.merge(stage[period_back],tmp_dfv2[max_period-period_back], on='indice', how='left')
			stage[period_back]=pd.merge(tmp_dfv2[max_period-period_back],stage[period_back], on='indice', how='left')
			stage_tmp=stage[period_back]
			max=max_period-period_back+2
			fact=2*(max_period-period_back)
			sup=max*(4)+fact
			campos.extend([0,sup-1,sup])			
			#print(campos)
			
			#for comb in range(combinations):
				#print(comb)	
				#max=max_period-period_back+2
				#print(max)
		elif period_back== 0:
			for i in reversed (range(max_period-period_back+1)):			
				stage_tmp.columns=stage_tmp.columns.str.replace('-'+str(i),'-'+str(i+1))
			#stage_tmp=pd.merge(stage_tmp,tmp_dfv1[max_period-period_back], on='indice', how='left')
			stage[period_back]=pd.merge(tmp_dfv1[max_period-period_back],stage_tmp, on='indice', how='left', suffixes=['_l', '_r'])
			stage_tmp.rename(columns={'FECHA_x':'V2_FECHA','MEDIA_x':'V2_MEDIA','ERROR_x':'V2_ERROR'},inplace=True)
			stage_tmp.rename(columns={'FECHA_y':'V1_FECHA','MEDIA_y':'V1_MEDIA','ERROR_y':'V1_ERROR'},inplace=True)
			#stage_tmp.rename(columns={'FECHA_x':'V1_FECHA-'+(num_periods_back),'MEDIA_x':'V1_MEDIA-'+(num_periods_back),'ERROR_x':'V1_ERROR-'+(num_periods_back)},inplace=True)
			#stage_tmp.rename(columns={'FECHA_y':'V2_FECHA-'+(num_periods_back),'MEDIA_y':'V2_MEDIA-'+(num_periods_back),'ERROR_y':'V2_ERROR-'+(num_periods_back)},inplace=True)
			for comb in range(combinations):
				#print(comb)	
				if comb==0:
					campos=[i for i in range(len(stage_tmp.columns)-1)]
					campos.pop(0)
					for i in range (1,len(campos)-2,3):
						campos.remove(i)
						campos_print=campos[:]
						campos_print.insert(0,campos[-2])
						campos_print.pop(-2)
						stage2=stage_tmp.iloc[:,pd.eval(campos_print)]
						stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print (campos)
				if comb==1:
					for i in range (3,campos[-1]-1,3):
						campos.remove(i)
						campos_print=campos[:]
						campos_print.insert(0,campos[-2])
						campos_print.pop(-2)
						stage2=stage_tmp.iloc[:,pd.eval(campos_print)]
						stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print (campos)
				if comb==2:
					campos.pop(0)
					campos_print=campos[:]
					campos_print.insert(0,campos[-2])
					campos_print.pop(-2)
					stage2=stage_tmp.iloc[:,pd.eval(campos_print)]
					stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print (campos)
				if comb==3:
					campos_aux.append(campos[0])
					campos_aux.append(campos[0]+1)
					campos.pop(0)	
					campos.insert(0,campos_aux[1])
					campos.insert(0,campos_aux[0])
					campos_print=campos[:]
					campos_print.insert(0,campos[-2])
					campos_print.pop(-2)
					stage2=stage_tmp.iloc[:,pd.eval(campos_print)]
					stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print(campos)				
			
		else:
			for i in reversed (range(max_period-period_back+1)):			
				stage_tmp.columns=stage_tmp.columns.str.replace('-'+str(i),'-'+str(i+1))
			#stage_tmp=pd.merge(stage_tmp,tmp_dfv1[max_period-period_back], on='indice', how='left')
			stage[period_back]=pd.merge(tmp_dfv1[max_period-period_back],stage_tmp, on='indice', how='left', suffixes=['_l', '_r'])
			#stage_tmp.rename(columns={'FECHA_x':'V2_FECHA-'+str((max_period-period_back+1)),'MEDIA_x':'V2_MEDIA-'+str((max_period-period_back+1)),'ERROR_x':'V2_ERROR-'+str((max_period-period_back+1))},inplace=True)
			#stage_tmp.rename(columns={'FECHA_y':'V1_FECHA-'+str((max_period-period_back+1)),'MEDIA_y':'V1_MEDIA-'+str((max_period-period_back+1)),'ERROR_y':'V1_ERROR-'+str((max_period-period_back+1))},inplace=True)
			stage_tmp.rename(columns={'FECHA_x':'V2_FECHA-1','MEDIA_x':'V2_MEDIA-1','ERROR_x':'V2_ERROR-1'},inplace=True)
			stage_tmp.rename(columns={'FECHA_y':'V1_FECHA-1','MEDIA_y':'V1_MEDIA-1','ERROR_y':'V1_ERROR-1'},inplace=True)
			for comb in range(combinations):
				#print(comb)	
				if comb==0:
					campos=[i for i in range(len(stage_tmp.columns)-1)]
					campos.pop(0)
					for i in range (1,len(campos)-2,3):
						campos.remove(i)
						campos_print=campos[:]
						campos_print.insert(0,campos[-2])
						campos_print.pop(-2)
						stage2=stage_tmp.iloc[:,pd.eval(campos_print)]
						stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print (campos)
				if comb==1:
					for i in range (3,campos[-1]-1,3):
						campos.remove(i)
						campos_print=campos[:]
						campos_print.insert(0,campos[-2])
						campos_print.pop(-2)
						stage2=stage_tmp.iloc[:,pd.eval(campos_print)]
						stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print (campos)
				if comb==2:
					campos.pop(0)
					campos_print=campos[:]
					campos_print.insert(0,campos[-2])
					campos_print.pop(-2)
					stage2=stage_tmp.iloc[:,pd.eval(campos_print)]
					stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print (campos)
				if comb==3:
					campos_aux.append(campos[0])
					campos_aux.append(campos[0]+1)
					campos.pop(0)	
					campos.insert(0,campos_aux[1])
					campos.insert(0,campos_aux[0])
					campos_print=campos[:]
					campos_print.insert(0,campos[-2])
					campos_print.pop(-2)
					stage2=stage_tmp.iloc[:,pd.eval(campos_print)]
					stage2.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'_'+desc[comb]+'.csv',index=False)			
					print(campos)				
			#stage_tmp.to_csv('S:\proyecto2\csv\SCENES\scene'+frec_scene+'-'+str((max_period-period_back+1))+'.csv',index=False)			
			#print(len(stage_tmp.columns))
			#stage_tmp=pd.merge(stage_tmp,tmp_dfv2[max_period-period_back], on='indice', how='left')
			stage_tmp=pd.merge(tmp_dfv2[max_period-period_back],stage_tmp, on='indice', how='left')
			#print (period_back)
			#print (num_periods_back)
			max=max_period-period_back+2
			fact=2*(max_period-period_back)
			sup=max*(4)+fact
			#print(sup)			
