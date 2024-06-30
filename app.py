import streamlit as st  
import pandas as pd 
import plotly.express as px 
import numpy as np 
import matplotlib.pyplot as plt
#%matplotlib inline
from matplotlib import style
import seaborn as sns   

nav=st.sidebar.radio("Navigation",["Women Population","Women Literacy","Women Health","Reproductive Health","Marriage and Remarriage","Infants, mortality and health","Consent and Violence"])

Mydata =pd.read_csv("NFHS_5_Factsheets_Data.csv")

if nav=="Women Literacy":
        st.title("Women Literacy")
        data1 = Mydata[['States/UTs','Women (age 15-49) who are literate4 (%)', 'Men (age 15-49) who are literate4 (%)']]
        
        #data cleaning
        data1 = data1.drop(index=range(3))
        # Convert columns to numeric
        numeric_columns = ['Women (age 15-49) who are literate4 (%)', 'Men (age 15-49) who are literate4 (%)']
        data1[numeric_columns] = data1[numeric_columns].apply(pd.to_numeric, errors='coerce')
        average_literacy_rates = data1.groupby('States/UTs').agg({'Women (age 15-49) who are literate4 (%)': 'mean', 'Men (age 15-49) who are literate4 (%)': 'mean'}).reset_index()
        # Display the formatted data
        #st.table(average_literacy_rates)

        #plotting graph
        xpos = np.arange(len(average_literacy_rates))
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(14, 9))
        barWidth = 0.4
        # plotting the bars
        ax.bar(xpos - barWidth / 2, average_literacy_rates['Women (age 15-49) who are literate4 (%)'], color='red', width=barWidth, label='Women Literacy')
        ax.bar(xpos + barWidth / 2, average_literacy_rates['Men (age 15-49) who are literate4 (%)'], color='royalblue', width=barWidth, label='Men Literacy')

        # Adding labels and title
        ax.set_xlabel('States/UTs')
        ax.set_ylabel('Literacy Rate (%)')
        ax.set_title('Literacy Rates of Men and Women in Every State/UT')
        ax.set_xticks(xpos)
        ax.set_xticklabels(average_literacy_rates['States/UTs'], rotation=90)
        ax.legend()
        st.pyplot(fig)
        st.subheader("Insights-")
        st.write("From the graph, it is visible that the literacy rate of women is less than the literacy rate of men in every state except Kerala, especially in the states of Bihar,  Jharkhand, Madhya Pradesh, Rajasthan, Telangana, Uttar Pradesh")

        
if nav == "Women Population":
        st.title("Sex Ratio Comparison - Urban, Rural, and Total")

        # Extracting data for plotting
        data2 = Mydata[['States/UTs', 'Area', ' Sex ratio of the total population (females per 1,000 males)']]
        data2 = data2.drop(index=range(3))

        # Data cleaning
        urban_data = data2[data2['Area'] == 'Urban']
        rural_data = data2[data2['Area'] == 'Rural']
        total_data = data2[data2['Area'] == 'Total']

        states = urban_data['States/UTs']
        urban_sex_ratio = urban_data[' Sex ratio of the total population (females per 1,000 males)']
        rural_sex_ratio = rural_data[' Sex ratio of the total population (females per 1,000 males)']
        total_sex_ratio = total_data[' Sex ratio of the total population (females per 1,000 males)']

        # Set a common length for all arrays
        common_length = min(len(states), len(urban_sex_ratio), len(rural_sex_ratio), len(total_sex_ratio))

        # Truncate or pad the data to the common length
        states = states[:common_length]
        urban_sex_ratio = urban_sex_ratio[:common_length]
        rural_sex_ratio = rural_sex_ratio[:common_length]
        total_sex_ratio = total_sex_ratio[:common_length]

        # Plotting a grouped bar graph
        fig, ax = plt.subplots(figsize=(10, 7))

        # Set width of the bars
        barWidth = 0.25

        # Set position of the bar on X axis
        r1 = np.arange(len(states))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]

        # Plotting the bars
        ax.bar(r1, urban_sex_ratio, color='blue', width=barWidth, edgecolor='grey', label='Urban')
        ax.bar(r2, rural_sex_ratio, color='orange', width=barWidth, edgecolor='grey', label='Rural')
        ax.bar(r3, total_sex_ratio, color='green', width=barWidth, edgecolor='grey', label='Total')

        # Adding labels and title
        ax.set_xlabel('States/UTs')
        ax.set_ylabel('Sex Ratio (females per 1,000 males)')
        ax.set_title('Sex Ratio Comparison - Urban, Rural, and Total')
        ax.set_xticks([r + barWidth for r in range(len(states))])
        ax.set_xticklabels(states, rotation=90)
        ax.legend()

        # Display the plot in Streamlit
        st.pyplot(fig)
        #insights
        st.subheader("Insights-")
        st.write("**1.Urban areas:** Lakshadweep has the highest sex ratio in urban areas, while Dadra and Nagar Haveli & Daman and Diu has the lowest. Other states with relatively higher sex ratios in urban areas include Kerala, Puducherry, Tamil Nadu, and Goa. States like Haryana, Chandigarh, and NCT of Delhi have lower sex ratios.")
        st.write("**2.Rural areas:** Lakshadweep, again, has the highest sex ratio in rural areas, while Dadra and Nagar Haveli & Daman and Diu has the lowest. Other states with relatively higher sex ratios in rural areas include Kerala, Tamil Nadu, Goa, and Puducherry. States like Chandigarh, Haryana, and NCT of Delhi have lower sex ratios.")
        st.write("**3.Regional Variation:**  Southern states like Kerala, Tamil Nadu, Karnataka, and Andhra Pradesh tend to have higher sex ratios compared to some northern states. Union territories like Lakshadweep and Puducherry consistently show higher sex ratios across all areas.")

if nav == "Women Health":
    st.title("Women Health\n")
    st.header("Comparing Obesity in women in rural and urban areas")

    # Remove non-numeric characters and replace empty strings with 0
    Mydata['Women (age 15-49 years) who are overweight or obese'] = Mydata['Women (age 15-49 years) who are overweight or obese'].str.replace(r'[^\d.]', '', regex=True).replace('', '0').astype(float)
    Mydata['Men (age 15-49 years) who are overweight or obese'] = Mydata['Men (age 15-49 years) who are overweight or obese'].str.replace(r'[^\d.]', '', regex=True).replace('', '0').astype(float)

    obesity_data = Mydata[['States/UTs', 'Area', 'Women (age 15-49 years) who are overweight or obese']]
    obesity_data=obesity_data.drop(index=range(3))
    obesity_data = obesity_data[obesity_data['Area'] != 'Total']
    #plotting the graph
    fig = px.bar(obesity_data, x="States/UTs", y="Women (age 15-49 years) who are overweight or obese",
    color="Area", hover_data=['Women (age 15-49 years) who are overweight or obese'],
             barmode='group')
    st.plotly_chart(fig)
    st.subheader("Insights - ")
    st.write("1. In many states, urban areas tend to have a higher percentage of overweight or obese women compared to their rural counterparts.")
    st.write("2. Union Territories like Chandigarh and NCT of Delhi show a relatively high prevalence of overweight or obese women, especially in urban areas. Chandigarh has the highest percentage in the urban category, while NCT of Delhi has high percentages in both urban and rural areas.")
    st.write("3. State Variations: States like Kerala, Goa, and Tamil Nadu exhibit a significant prevalence of overweight or obese women across all categories (urban, rural, total). These states consistently show higher percentages compared to the national average.")
    st.write("4. States like Kerala, Goa, and Tamil Nadu exhibit a significant prevalence of overweight or obese women across all categories (urban, rural)")
    st.write("5. States like Jharkhand, Meghalaya, and Nagaland generally have lower percentages of overweight or obese women, and the urban areas often have a higher prevalence than rural areas.")
    st.write("6. North-South Divide: Southern states like Kerala, Tamil Nadu, and Goa consistently show higher percentages of overweight or obese women compared to some northern states. This suggests a potential regional pattern in the prevalence of overweight or obesity.")




if nav=="Reproductive Health":
        st.header("Reproductive Health")
        data3=Mydata[['States/UTs', 'Area', 'Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Female sterilization (%)','Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Male sterilization (%)']]
        data4=data3.head(3)
        #st.table(data4)
        data4 = {
         'Category':['Female_sterilizatiuon_rural','Female_Sterilization_urban','Male_Sterilization_rural','Male_Sterilization_urban'],
          'Count':[38.7,36.3,0.3,0.2]
        }
        df=pd.DataFrame(data4)
        #plotting the pie chart
        st.subheader("Comparing the female and male sterilization in urban and rural areas")
        fig=px.pie(data4,values='Count',names='Category')
        st.plotly_chart(fig)
        st.subheader("Insights-")
        st.write("**1.Prevalence of Female Sterilization:** The data indicates that female sterilization is more prevalent than male sterilization, both in rural and urban areas. The percentages for female sterilization are significantly higher (38.7% in rural and 36.3% in urban) compared to male sterilization (0.3% in rural and 0.2% in urban).")
        st.write("**2.Urban vs. Rural Disparities:** While female sterilization is prevalent in both rural and urban areas, the percentages are slightly higher in rural regions. This could be due to various factors such as accessibility to healthcare facilities, awareness programs, and cultural practices.")
        st.write("**3.Low Prevalence of Male Sterilization:** The data shows a considerably lower prevalence of male sterilization compared to female sterilization. This might be attributed to factors such as awareness, cultural norms, and accessibility to male sterilization services.")
        st.write("**4.Policy Implications:** The data suggests a need for targeted family planning and reproductive health policies, with a focus on both rural and urban areas. Efforts to increase awareness about different sterilization options, especially male sterilization, may contribute to more balanced choices.")
        st.write("**5.Cultural and Societal Factors:** The low prevalence of male sterilization might be influenced by cultural norms, societal perceptions, and traditional gender roles. Understanding these factors is crucial for the development of effective family planning programs.")
        st.write("**6.Healthcare Access:** Disparities in prevalence between rural and urban areas may indicate variations in healthcare access and infrastructure. Improving access to reproductive health services in rural areas could contribute to more equitable outcomes.")

        #plot 2
        data5=Mydata[['Area','Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Female sterilization (%)','Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Male sterilization (%)','Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - IUD/PPIUD (%)','Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Pill (%)','Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Condom (%)','Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Injectables (%)']]
        st.write("\n")
        st.write("\n")
        st.subheader("Comparative analysis of various Family Planning methods used")
        data5=data5.head(3)
        family_planning={
                'Method':['Female sterilization in rural area','Male sterilization in rural area','IUD/PPIUD in rural area','Pills in rural area','Condoms in rural area','Injectables in rural area','Female sterilization in urban area','Male sterilization in urban area','IUD/PPIUD in urban area','Pills in urban area','Condoms in urban area','Injectables in urban area',],

                'Use':[38.7,0.3,1.8,5.4,7.6,0.6,36.3,0.2,2.7,4.4,13.6,0.4]
        }
        fig=px.pie(family_planning,values='Use',names='Method')
        st.plotly_chart(fig)
        #Insights 
        st.subheader("Insights - ")
        st.write("**1.IUD/PPIUD Usage:** The Intrauterine Device (IUD/PPIUD) is used as a family planning method, with varying percentages across different areas. Urban areas show the highest usage (2.7%), followed by total (2.1%), and rural (1.8%). While the percentages are not as high as female sterilization, there is some adoption of IUD/PPIUD.")
        st.write("**2.Pill Usage:** The pill is a commonly used family planning method, with relatively consistent percentages across urban, rural, and total categories. Urban areas have the highest usage (4.4%), followed by total (5.1%) and rural (5.4%).")
        st.write("**3.Condom Usage:** Condom usage is observed across all areas, with varying percentages. The data suggests that condom usage is relatively lower compared to other methods, such as female sterilization and the pill. Urban areas have the highest condom usage (13.6%), followed by total (9.5%) and rural (7.6%).")
        st.write("**4.Injectables Usage:** The use of injectables as a family planning method is visible, but the percentages are generally low across all areas. Urban areas show the highest usage (0.4%), followed by total (0.6%) and rural (0.6%).")
        st.write("**5.Urban-Rural Disparities:** There are differences in the prevalence of family planning methods between urban and rural areas. For instance, female sterilization is more prevalent in rural areas, while condom usage is higher in urban areas.")

        #Correlation plot

        data9=Mydata[['Women age 15-24 years who use hygienic methods of protection during their menstrual period26 (%)','Women (age 15-49 years) having a bank or savings account that they themselves use (%)','Women (age 15-49)  with 10 or more years of schooling (%)','Women (age 15-49) who are literate4 (%)','Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Any method6 (%)','Health worker ever talked to female non-users about family planning (%)']]

        # Data cleaning: handling the missing values and converting string '(0.0)' to NaN
        data9.replace(['*', '(69.2)', '(0.0)'], pd.NA, inplace=True)

        # Drop rows with missing values
        data9.dropna(inplace=True)

        # Convert the DataFrame to numeric, handling any remaining string values
        data9 = data9.apply(pd.to_numeric, errors='coerce')

        #st.table(req_data)
        # Calculate the correlation matrix
        correlation = data9.corr()
        #st.write(correlation)
        # Plot the heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation, annot=True, cmap='YlGnBu', linewidths=.5)
        # Display the plot using st.pyplot() with the figure argument
        st.subheader("Correlation between Period hygine, Women Literacy, Education and Family Planning, awareness spread by health workers")
        st.pyplot(plt)
        st.subheader("Insights")
        st.write("1.There is a strong positive correlation (0.7453) between Women age 15-24 years who use hygienic methods of protection during their menstrual period and Women (age 15-49) with 10 or more years of schooling. This implies that women who have more years of schooling are more likely to use hygienic methods during their menstrual period.")
        st.write("2.There is a positive correlation (0.4413) between Women age 15-24 years who use hygienic methods of protection during their menstrual period and Women (age 15-49 years) having a bank or savings account that they themselves use. This suggests that there might be a tendency for women who use hygienic methods during their menstrual period to also have a bank or savings account.")
        st.write("3.There is a positive correlation (0.2274) between Current Use of Family Planning Methods and Health worker ever talked to female non-users about family planning, indicating that women who use family planning methods are more likely to have had discussions with health workers.")
        st.write("There is a positive correlation (0.5863) between Women age 15-24 years who use hygienic methods of protection during their menstrual period and Women (age 15-49) who are literate. This suggests a positive association between literacy and the use of hygienic methods during menstruation.")


if nav=='Marriage and Remarriage':
       #Correlation plot
        req_data=Mydata[['Female population age 6 years and above who ever attended school (%)','Women age 20-24 years married before age 18 years (%)','Men age 25-29 years married before age 21 years (%)','Women age 15-19 years who were already mothers or pregnant at the time of the survey (%)','Women (age 15-49) who are literate4 (%)','Men (age 15-49) who are literate4 (%)']]
        # Data cleaning: handling the missing values and converting string '(0.0)' to NaN
        req_data.replace(['*', '(69.2)', '(0.0)'], pd.NA, inplace=True)

        # Drop rows with missing values
        req_data.dropna(inplace=True)

        # Convert the DataFrame to numeric, handling any remaining string values
        req_data = req_data.apply(pd.to_numeric, errors='coerce')

        #st.table(req_data)
        # Calculate the correlation matrix
        st.title("Child Marriage, teenage pregnancy and literacy")
        correlation = req_data.corr()
        #st.write(correlation)
        # Plot the heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation, annot=True, cmap='coolwarm', linewidths=.5)
        # Display the plot using st.pyplot() with the figure argument
        st.pyplot(plt)

        # Write insights based on the analysis
        st.write("**1.Positive Correlations:** The correlation between Female population age 6 years and above who ever attended school (%) and Women (age 15-49) who are literate (%) is 0.954, indicating a strong positive correlation. This suggests that as the percentage of females attending school increases, the percentage of literate women also tends to increase.There is a strong positive correlation (0.8019) between Men (age 15-49) who are literate (%) and Women (age 15-49) who are literate (%).")

        st.write("**2.Negative Correlations:** A negative correlation exists (-0.7449) between Women (age 20-24 years) married before age 18 years (%) and Men (age 15-49) who are literate (%). This implies that a higher percentage of women married before the age of 18 is associated with a lower percentage of literate men. The correlation between Men age 25-29 years married before age 21 years (%) and Women (age 15-19 years) who were already mothers or pregnant at the time of the survey (%) is negative (-0.7177), suggesting a tendency for fewer men marrying before age 21 when there is a higher percentage of young women who are already mothers or pregnant.")
       

if nav=="Infants, mortality and health":
        required_data=Mydata[['Mothers who had an antenatal check-up in the first trimester  (for last birth in the 5 years before the survey) (%)',
        'Mothers who had at least 4 antenatal care visits  (for last birth in the 5 years before the survey) (%)',
        'Mothers who consumed iron folic acid for 100 days or more when they were pregnant (for last birth in the 5 years before the survey) (%)',
        'Mothers who consumed iron folic acid for 180 days or more when they were pregnant (for last birth in the 5 years before the survey} (%)',
        'Registered pregnancies for which the mother received a Mother and Child Protection (MCP) card (for last birth in the 5 years before the survey) (%)',
        'Mothers who received postnatal care from a doctor/nurse/LHV/ANM/midwife/other health personnel within 2 days of delivery (for last birth in the 5 years before the survey) (%)',
        'Ever-married women age 18-49 years who have experienced physical violence during any pregnancy (%)',
        'Neonatal mortality rate (per 1000 live births)',
        'Infant mortality rate (per 1000 live births)']]
        # Data cleaning: handling the missing values and converting string '(0.0)' to NaN
        required_data.replace(['*', '(69.2)', '(0.0)'], pd.NA, inplace=True)

        # Drop rows with missing values
        required_data.dropna(inplace=True)

        # Convert the DataFrame to numeric, handling any remaining string values
        required_data = required_data.apply(pd.to_numeric, errors='coerce')

        # Display the cleaned DataFrame
        #st.table(req_data)

        # Calculate the correlation matrix
        correlation = required_data.corr()
        #st.write(correlation)
        # Plot the heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation, annot=True, cmap='viridis', linewidths=.5)
        # Display the plot using st.pyplot() with the figure argument
        st.subheader("understanding of the relationships between different maternal healthcare indicators and mortality rates")
        st.pyplot(plt)
        st.subheader("Insights")
        st.write("1.Mothers who had an antenatal check-up in the first trimester (%) and Mothers who had at least 4 antenatal care visits (%):There is a strong positive correlation of 0.76 between these two variables.This suggests that mothers who had an antenatal check-up in the first trimester are more likely to have had at least 4 antenatal care visits.")
        st.write("2.Mothers who had at least 4 antenatal care visits (%) and Mothers who consumed iron folic acid for 100 days or more when they were pregnant (%):There is a positive correlation of 0.73 between these two variables.Mothers who attended at least 4 antenatal care visits are more likely to have consumed iron folic acid for an extended duration during pregnancy.")
        st.write("3.Mothers who consumed iron folic acid for 100 days or more and Mothers who consumed iron folic acid for 180 days or more:There is a very high positive correlation of 0.90 between these two variables.Mothers who consumed iron folic acid for 100 days or more are highly likely to have continued for 180 days or more.")
        st.write("4.Mothers who had an antenatal check-up in the first trimester (%) and Mothers who received postnatal care within 2 days of delivery (%):There is a strong positive correlation of 0.80 between these two variables.Mothers who had early antenatal check-ups are more likely to receive postnatal care promptly after delivery.")
        st.write("5.Ever-married women age 18-49 years who have experienced physical violence during any pregnancy (%) and Neonatal Mortality Rate:There is a positive correlation of 0.26 between these two variables. Regions with higher rates of physical violence during pregnancy tend to have a slightly higher neonatal mortality rate.")
        st.write("6.Neonatal Mortality Rate and Infant Mortality Rate:There is a very high positive correlation of 0.96 between these two variables. Regions with higher neonatal mortality rates also tend to have higher infant mortality rates, indicating a strong association between these two measures.")

if nav=="Consent and Violence":
        data_for_analysis=Mydata[['Ever-married women age 18-49 years who have ever experienced spousal violence27 (%)',
        'Currently married women (age 15-49 years) who usually participate in three household decisions25 (%)',
        'Young women age 18-29 years who experienced sexual violence by age 18 (%)',
        'Female population age 6 years and above who ever attended school (%)',
        'Women (age 15-49) who are literate4 (%)',
        'Men (age 15-49) who are literate4 (%)',
        'Women (age 15-49)  with 10 or more years of schooling (%)',
        'Men (age 15-49)  with 10 or more years of schooling (%)']]
        # Data cleaning: handling the missing values and converting string '(0.0)' to NaN
        data_for_analysis.replace(['*', '(69.2)', '(0.0)'], pd.NA, inplace=True)

        # Drop rows with missing values
        data_for_analysis.dropna(inplace=True)

        # Convert the DataFrame to numeric, handling any remaining string values
        data_for_analysis = data_for_analysis.apply(pd.to_numeric, errors='coerce')

        # Display the cleaned DataFrame
        #st.table(req_data)

        # Calculate the correlation matrix
        correlation = data_for_analysis.corr()
        #st.write(correlation)
        # Plot the heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation, annot=True, cmap='cividis', linewidths=.5)
        # Display the plot using st.pyplot() with the figure argument
        st.subheader("relationships between various indicators related to violence, decision-making, education, and literacy rates")
        st.pyplot(plt)
        st.subheader("Insights")
        st.write("1.Ever-married women age 18-49 years who have ever experienced spousal violence27 (%) and Currently married women who usually participate in three household decisions25 (%): There is a negative correlation of -0.35 between these two variables.It suggests that, in general, women who have experienced spousal violence are less likely to participate in household decisions.")
        st.write("2.Young women age 18-29 years who experienced sexual violence by age 18 (%) and Female population age 6 years and above who ever attended school (%):There is a positive correlation of 0.32 between these two variables.Regions with higher rates of young women experiencing sexual violence tend to have a higher percentage of females who have attended school.")
        st.write("3.Women (age 15-49) who are literate4 (%) and Men (age 15-49) who are literate4 (%):There is a high positive correlation of 0.81 between these two variables.Both women and men show a strong correlation in literacy rates.")
        st.write("4.Women (age 15-49) with 10 or more years of schooling (%) and Men (age 15-49) with 10 or more years of schooling (%): There is a very high positive correlation of 0.91 between these two variables.The correlation suggests that the education levels of women and men with 10 or more years of schooling are highly correlated.")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")

        # Comparing violence in rural and urban area
        st.header("Comparing spousal violence experienced by women in rural and urban area")
        st.write("\n")
        st.write("\n")

        violence_data = Mydata[['States/UTs', 'Area', 'Ever-married women age 18-49 years who have ever experienced spousal violence27 (%)', 'Young women age 18-29 years who experienced sexual violence by age 18 (%)']]
        violence_data = violence_data.drop(index=range(3))
        # Data cleaning
        urban_data = violence_data[violence_data['Area'] == 'Urban']
        rural_data = violence_data[violence_data['Area'] == 'Rural']
        total_data = violence_data[violence_data['Area'] == 'Total']
        states = urban_data['States/UTs']

        violence_in_urban_area= urban_data['Ever-married women age 18-49 years who have ever experienced spousal violence27 (%)']
        violence_in_rural_area= rural_data['Ever-married women age 18-49 years who have ever experienced spousal violence27 (%)']

        violence_in_urban_area = pd.to_numeric(violence_in_urban_area, errors='coerce')
        violence_in_rural_area = pd.to_numeric(violence_in_rural_area, errors='coerce')

        
        # Display the separated DataFrames
        #st.table(urban_data)
        #st.table(rural_data)
        #st.table(total_data)


        # Set a common length for all arrays
        common_length = min(len(states), len(violence_in_urban_area), len(violence_in_rural_area))

        # Truncate or pad the data to the common length
        states = states[:common_length]
        violence_in_urban_area = violence_in_urban_area[:common_length]
        violence_in_rural_area = violence_in_rural_area[:common_length]

        # Plotting a grouped bar graph
        fig, ax = plt.subplots(figsize=(10, 7))

        # Set width of the bars
        barWidth = 0.30

        # Set position of the bar on X axis
        r1 = np.arange(len(states))
        r2 = [x + barWidth for x in r1]

        # Plotting the bars
        ax.bar(r1, violence_in_urban_area, color='green', width=barWidth, edgecolor='grey', label='Urban')
        ax.bar(r2, violence_in_rural_area, color='red', width=barWidth, edgecolor='grey', label='Rural')

        # Adding labels and title
        ax.set_xlabel('States/UTs')
        ax.set_ylabel('Ever-married women age 18-49 years who have ever experienced spousal violence(%)')
        ax.set_title('Comparison of spousal violence in rural and urban areas')
        ax.set_xticks([r + barWidth for r in range(len(states))])
        # Set y-axis ticks at intervals of 10
        tick_interval = 10
        max_value = np.nanmax([np.nanmax(violence_in_urban_area), np.nanmax(violence_in_rural_area)])
        ax.set_yticks(range(0, int(max_value) + 1, tick_interval))
        ax.set_xticklabels(states, rotation=90)
        ax.legend()

        # Display the plot in Streamlit
        st.pyplot(fig)
        #insights
        st.write("Almost in all states except in the sates of Bihar and Karnataka, spousal violence faced by the women is more in rural areas than in urban areas. Comaritively, more women in the states of Karnataka, Bihar, Manipur,Tamilnadu and Telangana have reported to experience spousal violence.")
        st.write("\n")
        st.write("\n")
        st.write("\n")
        st.write("\n")

        # Comparing violence in rural and urban area
        st.header("Comparitive study of sexual violence experienced by women  in rural and urban area")
        st.write("\n")
        st.write("\n")

        sexual_violence_data = Mydata[['States/UTs', 'Area','Young women age 18-29 years who experienced sexual violence by age 18 (%)']]
        Mydata = Mydata.drop(index=range(3))
        # Data cleaning
        urban_data = sexual_violence_data[sexual_violence_data['Area'] == 'Urban']
        rural_data = sexual_violence_data[sexual_violence_data['Area'] == 'Rural']
        states = urban_data['States/UTs']
        violence_in_urban_area= urban_data['Young women age 18-29 years who experienced sexual violence by age 18 (%)']
        violence_in_rural_area= rural_data['Young women age 18-29 years who experienced sexual violence by age 18 (%)']

        violence_in_urban_area = pd.to_numeric(violence_in_urban_area, errors='coerce')
        violence_in_rural_area = pd.to_numeric(violence_in_rural_area, errors='coerce')

        # Set a common length for all arrays
        common_length = min(len(states), len(violence_in_urban_area), len(violence_in_rural_area))

        # Truncate or pad the data to the common length
        states = states[:common_length]
        violence_in_urban_area = violence_in_urban_area[:common_length]
        violence_in_rural_area = violence_in_rural_area[:common_length]

        # Plotting a grouped bar graph
        fig, ax = plt.subplots(figsize=(10, 7))

        # Set width of the bars
        barWidth = 0.30

        # Set position of the bar on X axis
        r1 = np.arange(len(states))
        r2 = [x + barWidth for x in r1]

        # Plotting the bars
        ax.bar(r1, violence_in_urban_area, color='dodgerblue', width=barWidth, edgecolor='grey', label='Urban')
        ax.bar(r2, violence_in_rural_area, color='crimson', width=barWidth, edgecolor='grey', label='Rural')

        # Adding labels and title
        ax.set_xlabel('States/UTs')
        ax.set_ylabel('Young women age 18-29 years who experienced sexual violence by age 18(%)')
        st.write("\n")
        st.write("\n")
        ax.set_title('Comparison of sexual violence experienced by women in rural and urban areas')
        ax.set_xticks([r + barWidth for r in range(len(states))])
        # Set y-axis ticks at intervals of 10
        tick_interval = 2
        max_value = np.nanmax([np.nanmax(violence_in_urban_area), np.nanmax(violence_in_rural_area)])
        ax.set_yticks(range(0, int(max_value) + 1, tick_interval))
        ax.set_xticklabels(states, rotation=90)
        ax.legend()

        # Display the plot in Streamlit
        st.pyplot(fig)
        st.subheader("Insights - ")
        st.write("**1.Regional Variation**: There is significant regional variation in the percentage of young women (age 18-29 years) who experienced sexual violence by age 18. For example, states like Karnataka, Meghalaya, and West Bengal have higher percentages compared to states like Himachal Pradesh, Sikkim, and Tamil Nadu.")
        st.write("**2.Urban vs. Rural Disparities**: In some states, there is a noticeable difference in the prevalence of sexual violence between urban and rural areas. For instance, in Karnataka and Telangana, the urban areas exhibit higher percentages than their rural counterparts. On the other hand, in states like Bihar and Himachal Pradesh, rural areas have higher percentages.")
        st.write("**3.States with Zero or Low Incidence**: Some states, particularly in the south like Kerala, Tamil Nadu, and Puducherry, report zero or very low percentages of young women experiencing sexual violence. This might indicate better safety measures or reporting mechanisms in these regions.")
        st.write("States with Missing Data: Chandigarh and NCT of Delhi have missing or incomplete data. It's essential to address these gaps for a comprehensive analysis.")
        st.write("**Policy Implications**: States with higher percentages may need targeted interventions and awareness programs to address the issue of sexual violence against young women. Understanding the factors contributing to these variations can help formulate effective policies.")

       