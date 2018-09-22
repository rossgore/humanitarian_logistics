from model_explorer import ModelExplorer 

# create model and adjust param

test = ModelExplorer(p_po_uniform=False, p_width=200, p_height=200, p_num_pols=2, p_city_size=20, p_number_steps=1000, p_shock_flag =False, p_decision_quality=True, p_cultural_wellbeing=True)

test.trace_driver()

