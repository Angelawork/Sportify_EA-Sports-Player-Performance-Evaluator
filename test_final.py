from flask import Flask, render_template, request
import pandas as pd
import joblib
import sklearn

app = Flask(__name__)

model = joblib.load("random_forest_model(1).pkl")
#joblib.dump(model, "random_forest_model(1).pkl", protocol=3)


# Function that deals with input data (replace with your actual function)
# def process_input(input_data):
#     # Your processing logic here
#     return f"{input_data}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            input_data = int(request.form["input_data"])
            result, work_rate = get_prediction(input_data)
            return render_template("index.html", result=result, work_rate=work_rate)
        except ValueError:
            error_message = "Player not found. Please enter a valid player name."
            return render_template("index.html", error_message=error_message)
    return render_template("index.html", result=None)

def get_prediction(inputs):

  df = pd.read_csv('male_players.csv')
  model = joblib.load("random_forest_model (1).pkl")
  #joblib.dump(model, "random_forest_model(1).pkl", protocol=3)
  work_rate=[]
  output=[]
  for i in range(len(inputs)):
    player_name = inputs[i].strip()
    if player_name in df['long_name'].values:
        player_data = df.loc[df['long_name'] == player_name, ['fifa_version', 'overall', 'potential', 'value_eur',
                                                                'wage_eur', 'age', 'height_cm', 'weight_kg',
                                                                'club_team_id', 'league_id', 'league_level',
                                                                'nation_team_id', 'mentality_vision',
                                                                'power_stamina', 'work_rate']]

    else:
        print("Player not found in the database.")
        continue

    df_temp=player_data[player_data['fifa_version']==24.0]
    df_temp.fillna(0, inplace=True)
    df_temp.columns = ['fifa_version_year1', 'overall_year1', 'potential_year1', 'value_eur_year1', 'wage_eur_year1', 'age_year1',
          'height_cm_year1', 'weight_kg_year1', 'club_team_id_year1', 'league_id_year1', 'league_level_year1',
          'nation_team_id_year1', 'mentality_vision_year1', 'power_stamina_year1', 'work_rate']
    X=df_temp.drop(['work_rate','power_stamina_year1'],axis=1)
    prediction = model.predict(X)
    output.append([player_name,prediction])
    work_rate.append(player_data['work_rate'].tolist())
  for sublist in output:
    sublist[1] = float(sublist[1][0])
  result_string = '\n'.join(['{} {}'.format(sublist[0], sublist[1]) for sublist in output])
  #output= [array.tolist() for array in output]
  #output=[item for sublist in output for item in sublist]
  return result_string
  

if __name__ == "__main__":
    app.run(debug=True)