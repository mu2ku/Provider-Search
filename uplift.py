from flask import Flask, request, render_template
import json

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def home():
  gender = [] #empty list for gender
  primary_skills = [] #empty list for primary skills
  secondary_skills = [] #empty list for secondary skills
  f = open('providers.json')  #open JSON file
  providers = json.load(f) #return JSON object as a dictionary
  providers.sort(key=lambda x: x['rating'], reverse=True) #sorts providers from greatest to least
  
  #fill list of all primary skills
  for provider in providers:
    for skill in provider['primary_skills']:
      if skill not in primary_skills:
       primary_skills.append(skill)
  
  #fill list of all secondary skills
  for provider in providers:
    for skill in provider['secondary_skill']:
      if skill not in secondary_skills:
       secondary_skills.append(skill)
  
  #fill list of all genders
  for provider in providers:
    if provider['sex'] not in gender:
      gender.append(provider['sex'])
  
  return render_template('home.html', providers=providers, gender=gender, primary_skills=primary_skills, secondary_skills=secondary_skills)

@app.route("/results/", methods=['POST'])
def results():
  gender=[] #empty list for gender
  primary_skills = [] #empty list for primary skills
  secondary_skills = [] #empty list for secondary skills
  
  f = open('providers.json')  #open JSON file
  providers = json.load(f) #return JSON object as a dictionary
  
  #fill list of all genders
  for provider in providers:
    if provider['sex'] not in gender:
      gender.append(provider['sex'])
  
  #fill list of all primary skills   
  for provider in providers:
    for skill in provider['primary_skills']:
      if skill not in primary_skills:
        primary_skills.append(skill)

  #fill list of all secondary skills
  for provider in providers:
    for skill in provider['secondary_skill']:
      if skill not in secondary_skills:
        secondary_skills.append(skill)

  first_pass = [] #empty results list to contain filtered results
  second_pass = [] #empty results list to contain filtered results
  third_pass = [] #empty results list to contain filtered results
  fourth_pass = [] #empty results list to contain filtered results
  fifth_pass = [] #empty results list to contain filtered results
  
  if request.method == "POST":
    sex = request.form.getlist('sex') #retrieve selected gender from request form as a list
    active = request.form.getlist('active') #retrieve selected active status from request form as a list
    language = request.form.getlist('language') #retrieve selected language from request form as a list
    primary = request.form.getlist('primary') #retrieve selected primary skills from request form as a list
    secondary = request.form.getlist('secondary') #retrieve selected secondary skills from request form as a list
    
    #iterate over all providers. If provider gender is in request form append to first_pass list
    for provider in providers:
      if provider['sex'] in sex:
        first_pass.append(provider)
    
    #if first_pass exists, set it equal to providers. Otherwise, continue on to second pass
    if first_pass:
      providers = first_pass
    
    #iterate over all providers. If provider language is in request form append to second_pass list        
    for provider in providers:
      if provider['language'] in language:
        second_pass.append(provider)
    
    #if second_pass exists, set it equal to providers. Otherwise, continue on to third pass    
    if second_pass:
      providers = second_pass
      
    #iterate over all providers. If provider primary skills are in request form append to third_pass list
    for provider in providers:
      for skill in provider['primary_skills']:
        if skill in primary:
          third_pass.append(provider)
    
    #if third_pass exists, set it equal to providers. Otherwise, continue on to fourth pass  
    if third_pass:
      providers = third_pass
    
    #iterate over all providers. If provider secondary skills are in request form append to fourth_pass list
    for provider in providers:
      for skill in provider['secondary_skill']:
        if skill in secondary:
          fourth_pass.append(provider)
    
    #if fourth_pass exists, set it equal to providers. Otherwise, continue on to fifth pass 
    if fourth_pass:
      providers = fourth_pass
    
    #if "active" is in request form, check if provider active status is set to true. If so, append to fifth_pass list        
    if "active" in active:
      for provider in providers:
        if provider['active'] == True:
          fifth_pass.append(provider)
    
    #if "inactive" is in request form, check if provider active status is set to false. If so, append to fifth_pass list 
    if "inactive" in active:
      for provider in providers:
        if provider['active'] == False:
          fifth_pass.append(provider)
    
    #if fifth_pass exists, set it equal to providrs
    if fifth_pass:
      providers = fifth_pass
    #else if fifth_pass does not exist and active status was not part of the request form, pass
    elif not fifth_pass and not active:
      pass
    #else if fifth_pass does not exist but active status was part of the request form set providers equal to an empty list for no results
    elif not fifth_pass and active:
      providers = []
           
  providers.sort(key=lambda x: x['rating'], reverse=True) #sorts providers from greatest to least rating using a lambda function
  
  return render_template('home.html', providers=providers, gender=gender, primary_skills=primary_skills, secondary_skills=secondary_skills)