import numpy as np
import mesa
from model import HumanitarianLogistics, COA, AZC, Newcomer, City, NGO, IND
import activity
from Values import Values
import random
import csv
import traceback

class ModelExplorer():

    def __init__(self, p_po_uniform= False, p_width=200, p_height=200, p_num_pols=2, p_city_size=20, 
                 p_number_steps=500, p_shock_flag =False, p_decision_quality=True, p_cultural_wellbeing=True):

        self.width = p_width
        self.po_uniform = p_po_uniform
        self.height = p_height
        self.num_pols = p_num_pols
        self.city_size = p_city_size
        self.number_steps = p_number_steps
        self.shock_flag = p_shock_flag
        self.dq = p_decision_quality
        self.cultural_wellbeing = p_cultural_wellbeing
        
    def trace_driver(self):
        filename = 'spring-sim-trace-validation.csv'
        
        myData = [["trial_id", "step", "coa_se_value", "coa_st_value", "coa_c_value", "coa_otc_value", "ngo_se_value", "ngo_st_value", "ngo_c_value", "ngo_otc_value", "ind_se_value", "ind_st_value", "ind_c_value", "ind_otc_value", "cw_value", "ngo_p_value", "nc_p_value", "nc_wellbeing", "ctpo"]]
        
        coa_se = list(range(20, 80, 5))
        coa_st = list(range(20, 80, 5))
        coa_c = list(range(20, 80, 5))
        coa_otc = list(range(20, 80, 5))
        
        ngo_se = list(range(20, 80, 5))
        ngo_st = list(range(20, 80, 5))
        ngo_c = list(range(20, 80, 5))
        ngo_otc = list(range(20, 80, 5))
        
        ind_se = list(range(20, 80, 5))
        ind_st = list(range(20, 80, 5))
        ind_c = list(range(20, 80, 5))
        ind_otc = list(range(20, 80, 5))
        
        p_cw_group = ['A', 'C']
        
        ngo_present = [True, False]
        nc_participates = [True, False]
        
        myFile = open(filename, 'w')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(myData)
                   
        i = 0
        for cse in coa_se:
            for cst in coa_st:
                for cc in coa_c:
                    for cotc in coa_otc:
                        for nse in ngo_se:
                            for nst in ngo_st:
                                for nc in ngo_c:
                                    for notc in ngo_otc:
                                        for ise in ind_se:
                                            for ist in ind_st:
                                                for ic in ind_c:
                                                    for iotc in ind_otc:
                                                        for cw in p_cw_group:
                                                            for ngo_p in ngo_present:
                                                                for nc_p in nc_participates:
                                                                    params = [cse, cst, cc, cotc, nse, nst, nc, notc, ise, ist, ic, iotc, cw, ngo_p, nc_p]
                                                                    if (((cse+cst) == 100) and ((cc+cotc) ==100) and ((nse+nst)==100) and 
                                                                       ((nc+notc)==100) and ((ise+ist)==100) and ((ic+iotc)==100)):
                                                                        print(params)
                                                                        sim_values = self.trace(coa_se_value = cse, coa_st_value= cst, coa_c_value = cc, coa_otc_value = cotc, ngo_se_value = nse, ngo_st_value= nst, ngo_c_value = nc, ngo_otc_value = notc,ind_se_value = ise, ind_st_value=ist, ind_c_value=ic, ind_otc_value=iotc,cw_value = cw, ngo_p_value = ngo_p, nc_p_value = ncp, trial_id = i, all_time_steps = False)
                                                                        i = i + 1
                                                                        if sim_values is not None:
                                                                            for x in range(0, len(sim_values)):
                                                                                valuesToAdd = sim_values[x]
                                                                                if valuesToAdd is not None:
                                                                                    myFile = open(filename, 'a')
                                                                                    with myFile:
                                                                                        writer = csv.writer(myFile)
                                                                                        writer.writerows([valuesToAdd])
                                                                                    if sim_values is None:
                                                                                        print("Exception thrown during simulation run with: "+str(params))
    
    def trace(self, coa_se_value, coa_st_value, coa_c_value, coa_otc_value, ngo_se_value, ngo_st_value, ngo_c_value, ngo_otc_value,ind_se_value, ind_st_value, ind_c_value,cw_value, ngo_p_value, nc_p_value, all_time_steps, trial_id):
        toReturn = []
        test = HumanitarianLogistics(self.po_uniform, self.width, self.height, self.num_pols, self.city_size, self.coa_se, self.coa_st, self.coa_c, self.coa_otc,
                                     self.ngo_se, self.ngo_st, self.ngo_c, self.ngo_otc, self.ind_se, self.ind_st, self.ind_c, self.ind_otc)
        test.shock_flag = self.shock_flag
        test.dq = self.dq
        test.include_social_networks = False
        test.cultural_wellbeing = self.cultural_wellbeing
        test.cw_group = self.cw_group
            
        ngo = [x for x in test.schedule.agents if type(x) is NGO]
        coa_array = [coa for coa in test.schedule.agents if type(coa) is COA and coa.city.modality == 'AZC']
            
        inds = [ind for ind in test.schedule.agents if type(ind) is IND]
        azcs = [azc for azc in test.schedule.agents if type(azc) is AZC]
        cities = []
        for coa in coa_array:
            if coa.city is not None:
                cities.append(coa.city)
        if (ngo_p_value == False) or (nc_p_value == False):        
            for b in azcs:
                if po_value == -99:
                    b.city.ngo.funds = 0
                    b.funds = 0
                    b.city.ngo.testing = False
                    copy = set([])
                    for act in b.activity_center.activities_available:
                        if not (act.name == 'Football' or act.name == 'Volunteer'):
                            copy.add(act)
                            b.activity_center.activities_available = copy
        for step in range(0,self.number_steps):
            test.step()
            buf = []
            newcomers = [nc for nc in test.schedule.agents if type(nc) is Newcomer and nc.ls == 'as_ext']
            for nc in newcomers:
                buf.append(nc.values.health)
            nc_wellbeing = 100 - np.nanmean(buf_distress)
            ctpo = np.nanmean([city.public_opinion for city in cities])
            values = [trial_id, step, coa_se_value, coa_st_value, coa_c_value, coa_otc_value, ngo_se_value, ngo_st_value, ngo_c_value, ngo_otc_value,ind_se_value, ind_st_value, ind_c_value, cw_value, ngo_p_value, nc_p_value, nc_wellbeing, ctpo]
            if all_time_steps==True:
                toReturn.append(values)
        if all_time_steps == False:
            toReturn.append(values)
        return (toReturn)