from flask import Flask, render_template, request, send_file
import os 
from werkzeug.utils import secure_filename
import pandas as pd
import data_description
import handlig_null_values
import categorical
import feature_scaling

app = Flask(__name__)


app.config["CSV_upload"] = "E:/Info Objects/Project/Preprocessing/static/CSV"


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/task1", methods= ["POST","GET"])
def task1():
    if request.method == "POST":
        
        cf=request.files['file']

        filename = secure_filename(cf.filename)

        # basedir = os.path.abspath(os.path.dirname(__file__))
        # print(basedir)
        cf.save(os.path.join(app.config["CSV_upload"],filename))

        global df
        df=pd.read_csv('static/CSV/'+filename)
        s=list(df.columns)
        r=list(df.values[:,:])
        
        return render_template('task1.html', file=filename, data={"columns":s , "raws":r})
    return render_template('task1.html')


@app.route("/task2", methods=['GET',"POST"])
def task2():
    if request.method=="POST":
        id=request.form.get('submit')
        print(id)

        if id=="Submit":
            text=request.values['text']
            global df
            df.update(df.drop(columns=text,inplace=True))
            c=list(df.columns)
            return render_template("task2.html",data= c)
        else:
            c=list(df.columns)  
            return render_template("task2.html",data= c)
    return render_template("task2.html")


@app.route("/task3", methods= ["POST","GET"])
def task3():
    if request.method == "POST":
        s=list(df.columns)
        r=list(df.values[:,:])

        print(s)
        

        dc=request.form.get('dc')
        # print(dc)

        if dc=='1':
            df1 = data_description.desc(df)
            ind=list(df1.index)
            df.update(df1.insert(loc=0, column=" ", value=ind))
            print(df1)
            s=list(df1.columns)
            r=list(df1.values[:,:])
            return render_template('task3.html', data={"columns":s , "raws":r})

        elif dc=='2':
            text=request.values['text']
            # print(text)
            df1 =pd.DataFrame(data_description.desc_s(df,text))
            ind=list(df1.index)
            df.update(df1.insert(loc=0, column=" ", value=ind))
            print(df1)

            s=list(df1.columns)
            r=list(df1.values[:,:])
            return render_template('task3.html', data={"columns":s , "raws":r})


        elif dc=='3':
            # print(True)
            df1 = data_description.show_data(df)
            s=list(df1.columns)
            r=list(df1.values[:,:])
            return render_template('task3.html', data={"columns":s , "raws":r})


        return render_template('task3.html',data={"columns":s, "raws":r})
    return render_template('task3.html')


@app.route("/task4", methods=['GET',"POST"])
def task4():
    if request.method=="POST":
        s=list(df.columns)
        r=list(df.values[:,:])
        global c1
        c1=list(df.columns)

        name1=request.form.get('task1')
        name2=request.form.get('task2')
        name3=request.form.get('stat')
        id=request.form.get('submit')

        print(name1)
        print(name2)
        print(name3)
        print(id)

        if id=="Submit1":
            df.update(df.drop(columns=name1,inplace=True))
            c1.remove(name1)

            # df.update(handlig_null_values.remove_col(df,name1),inplace=True)
            s=list(df.columns)
            r=list(df.values[:,:])
            return render_template('task4.html', data={"columns":s , "raws":r,"c1":c1})

            
        elif id=="Click Here To See":
            c=[]
            for col in df.columns:
                c.append(col)
            df1=pd.DataFrame(handlig_null_values.f_null(df))
            df1.insert(loc=0, column="columns", value=c)
            df1.rename(columns={  0 : 'null_values'}, inplace=True)

            print(df1)
            s=list(df1.columns)
            r=list(df1.values[:,:])
            return render_template('task4.html', data={"columns":s , "raws":r,"c1":c1})

        elif id=="Submit2":
            if name3=="mean":
        
                df1=handlig_null_values.fill_na_mean(df,name2)
                df.update(df1)
                s=list(df.columns)
                r=list(df.values[:,:])
                return render_template('task4.html', data={"columns":s , "raws":r,"c1":c1})
        
            elif name3=="median":
                df1=handlig_null_values.fill_na_median(df,name2)
                df.update(df1)
                s=list(df.columns)  
                r=list(df.values[:,:])
                return render_template('task4.html', data={"columns":s , "raws":r,"c1":c1})


            elif name3=="mode":
                df1=handlig_null_values.fill_na_mode(df,name2)
                df.update(df1)
                s=list(df.columns)
                r=list(df.values[:,:])
                return render_template('task4.html', data={"columns":s , "raws":r,"c1":c1})
    

        return render_template("task4.html", data={"columns":s, "raws":r ,"c1":c1})
    return render_template("task4.html")


@app.route("/task5", methods=['GET',"POST"])
def task5():
    if request.method=="POST":
        s=list(df.columns)
        r=list(df.values[:,:])
        c1=list(categorical.categorical_info(df))


        name=request.form.get('submit')
        id=request.form.get('task')
        print(name)
        print(id)

        if name=="Submit":
            df1=pd.DataFrame(categorical.categorical_info(df))
            df1.rename(columns={  0 : 'Categorical_Columns'}, inplace=True)
            
            l=[]
            
            for i in df1['Categorical_Columns']:
                l.append(i)

            j=[]

            for i in l:
                uniqueValues = len(df[i].unique())
                # print(uniqueValues)
                j.append(uniqueValues)
                
            df1['Unique_Values']=j
            print(df1)
            s=list(df1.columns)
            r=list(df1.values[:,:])
            return render_template('task5.html', data={"columns":s , "raws":r, "c1":c1})

            
        if name=="Submit1": 
            df1=categorical.ohe(df,id)
            l=[]
            for i in df1:
                for j in df1[i]:
                    l.append(j)
                df[i]=l
                l.clear()
            df.update(df.drop(id,axis='columns'))
            print(df)
            s=list(df.columns)
            r=list(df.values[:,:])
            return render_template('task5.html', data={"columns":s , "raws":r, "c1":c1})

        return render_template("task5.html", data={"columns":s, "raws":r,"c1":c1 })
    return render_template("task5.html")


@app.route("/task6", methods= ["POST","GET"])
def task6():
    if request.method == "POST":
        s=list(df.columns)
        r=list(df.values[:,:])
        c1=list(df.columns)

        
        id=request.form.get('submit')
        name=request.form.get('col_name')
        name1=request.form.get('col_name1')

        print(id)
        print(name)
        print(name1)    

        if id=="Submit":
            df1=feature_scaling.minmax_df(df)
            print(df1)
            df.update(df1)
            print(df)
            s=list(df.columns)
            r=list(df.values[:,:])
            return render_template('task6.html', data={"columns":s , "raws":r, "c1":c1})


        if id=="Submit1":
            df1=feature_scaling.minmax_column(df,name)
            df.update(df1)
            print(df)
            s=list(df.columns)
            r=list(df.values[:,:])
            return render_template('task6.html', data={"columns":s , "raws":r, "c1":c1})

        if id=="Submit2":
            df1=feature_scaling.standardscaler_df(df)
            df.update(df1)
            print(df)
            s=list(df.columns)
            r=list(df.values[:,:])
            return render_template('task6.html', data={"columns":s , "raws":r, "c1":c1})

        if id=="Submit3":
            df1=feature_scaling.standardscaler_column(df,name1)
            df.update(df1)
            print(df)
            s=list(df.columns)
            r=list(df.values[:,:])
            return render_template('task6.html', data={"columns":s , "raws":r, "c1":c1})    

        return render_template('task6.html',data={"columns":s, "raws":r, "c1":c1})
    return render_template('task6.html',data={"columns":s, "raws":r, "c1":c1})



@app.route("/task7", methods= ["POST","GET"])
def task7():
    df.to_csv('static/CSV/preprocessed/preproccesd.csv')
    return send_file('static/CSV/preprocessed/preproccesd.csv',
                     mimetype='text/csv',
                     attachment_filename='Preproccesd.csv',
                     as_attachment=True)


@app.route("/features")
def features():
    return render_template('features.html') 

# if __name__=="__main__":
#     app.run(debug=True)