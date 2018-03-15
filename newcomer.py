import mesa 
from mesa import Agent, Model
from scipy.stats import bernoulli



class Newcomer(Agent):
    
    def __init__(self, unique_id, model,country_of_origin):
        
        '''
        
        Initializes Newcomer Class (NC)
        DQ - documentation quality
        pos - position in x,y space
        dq_min - refers to the IND standard
        decision time - time until IND must make a decision. 
        current_step - refers to what position the agent is in the sequence of actions
       
        
        '''
        super().__init__(unique_id, model)
        
        self.pos = None
        
        #ls is Legal Status
        self.ls = 'edp' #externally displaced person
        
        self.model.house(self) #place in ter apel
        
        self.decision_time = 28 #28 days is the length of the general asylum procedure
        
        self.intake_time = 4 #time until transfer out of ter apel
              
        self.coo = country_of_origin
        self.specs = self.model.specs[self.coo] #specs contains bournoulli distribution params
        
        self.ext_time = 90 #duration of extended procedure
        
        #draw first decision outcome
        self.first = bernoulli.rvs(self.specs[0], size = 1)[0] 
        #second decision outcome not drawn unless necessary
        self.second = None                                     
        
        
        
        
            
    def step(self):
        
        #EDP to AZ
        
        if self.ls == 'edp':
            self.intake_time -= 1
            
            if self.intake_time == 0:
                
                self.ls = 'as'
                self.model.house(self)
        
        
        
        #AZ to TR
        
        elif self.ls == 'as':
        
            self.decision_time -= 1
            
            if self.decision_time == 0:
                if self.first == 0:
                    self.ls = 'as_ext'
                    self.model.house(self)
                    
                    self.second = bernoulli.rvs(self.specs[1], size = 1)[0]
                    
                else:
                    self.ls = 'tr'
                    self.model.house(self)
                        
        # Extended Procedure to TR or Repatriation
        
        elif self.ls == 'as_ext':
            self.ext_time -= 1
            
            if self.ext_time == 0:
            
                if self.second == 0:
                    self.model.Remove(self)
                else:
                    self.ls = 'tr'
                    self.model.house(self)
         
       
        # Agent Temporary Resident            
        elif self.ls == 'tr':
            pass