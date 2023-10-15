#!/usr/bin/env python
# coding: utf-8

# 
# <div align="center"><font size="10">  
#      💻Udemy Courses 💻
# </font>
# </div>
# 
# <img decoding="async" fetchpriority="high" class="aligncenter size-full wp-image-166073" src="https://about.udemy.com/wp-content/uploads/2021/10/TURBO-ANIMATION-CONCEPT.gif" alt="" width="950" height="400">

# ## Introduction
# A renowned online learning portal, Udemy provides a huge selection of courses on a variety of subjects. Udemy has transformed how people study by giving both students and teachers a platform to connect from all over the world thanks to its user-friendly interface and accessibility.
# 
# Learners may choose from a wide range of courses in areas such as programming, business, the arts, personal development, and more, while teachers can impart their knowledge and skills to a worldwide audience. Udemy.com offers an accessible and adaptable learning experience for people of different backgrounds and interests, whether you're wanting to improve your abilities, follow a new hobby, or progress your career.

# ### In  this project
# 
# We will be exploring a dataset of of over 209,734 courses and 73,514 instructors teaching courses in 79 languages in 13 different categories.
# 
# We will be analyzing this dataset to gain insights into various aspects of courses , including :
# 
# The Popularity of Categories and Subcategories.
# 
# >1. Pricing Analysis.
# >2. Instructor Performance Analysis.
# >3. Time Analysis.

# ## Data Source
# The offered dataset includes a thorough compilation of data from user reviews and Udemy course comments. This dataset, which has 20 columns and a total of 209,734 items, provides insightful information about several facets of online learning. The columns include a variety of data kinds, such as text, boolean values, and floating-point integers.
# 
# Important columns contain information about course names, costs, subscribers, ratings, reviews, comments, and instructor profiles. The dataset also offers details about the course's duration, publication, update dates, category, subcategory, topic, language, and links to the sites of the teacher and the course.
# 

# ## Importing libraries

# In[1]:


import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# ## Loading  Dataset and Inspecting

# In[2]:


df1=pd.read_csv(r"C:\Users\nusut\Downloads\Udemy dataset\archive (7)\Course_info.csv")


# In[3]:


df1.head()


# In[4]:


for i in df1.columns.to_list():
    print(i)


# In[5]:


df1.info()


# In[6]:


df2=pd.read_csv(r"C:\Users\nusut\Downloads\Udemy dataset\archive (7)\Comments.csv")


# In[7]:


df2.head()


# In[8]:


df2.info()


# ## Finding duplicates  and null values

# In[9]:


dup_count=df1.duplicated().sum()
print(f"There are {dup_count} duplicate values are present in dataset")


# In[10]:


## finding the null values in dataset 
null_values=df1.isnull().sum()

## printing columns names having null values not equal to 0
null_values[null_values!=0]


# In[11]:


df1.shape


# In[12]:


null_value_percentage =pd.DataFrame(null_values[null_values !=0])


# In[13]:


null_value_percentage.reset_index()


# In[14]:


null_value_percentage.rename(columns={0:"null_value_count"},inplace=True)


# In[15]:


null_value_percentage["Percentage"] = round(((null_value_percentage["null_value_count"]/df1.shape[0])*100),2)


# In[16]:


null_value_percentage


# ## less than 1% null values are present in  dataset .

# In[17]:


df1.dropna(inplace=True)


# In[18]:


df1.head()


# ## Observing data for  Data cleaning and preprocessing
# 

# In[19]:


df1.columns


# In[20]:


df1.head()


# ### 'course_url','instructor_url'  are not need for our analysis so we remove those column  

# In[21]:


# droping course_ul and instructure_url 
df1.drop(['course_url','instructor_url'],axis=1, inplace=True)


# In[22]:


df1.head()


# ## Changing Datatypes 

# In[23]:


# some of the data types are in float need to change int and date time column are in string need to cahnge in datetime datatype 
dtype={
    'id' : "int", 
    'num_subscribers':"int64",
    'num_reviews':"int64",
    'num_comments':"int64",
    'num_lectures':"int64",
    'content_length_min' :"int64",
    'published_time' :"datetime64[ns]",
    'last_update_date' :"datetime64[ns]"
}


# In[24]:


df1=df1.astype(dtype)


# In[25]:


df1.info()


# In[26]:


df1.head()


# ## Exploratory Data Analysis
# 
# 
# 1. What is the most popular categories and subcategories?
# 
#     1.1 What is the most Popular Course in each category?
# 
# 
# 2. Pricing Analysis
# 
#     2.1 What is the distribution of courses price?
#     
#     2.2. What is the percentage of courses that are priced below 200 dollars on Udemy?
#     
#     
# 3. Instructor Performance Analysis.
#     
#    3.1. Who are the top 5 most performing instructors according to the number of subscribers?
#    
#    3.2. Who are the topmost 5 experienced instructors in terms of (Courses published  on Udemy)?
# 
# 
# 4. Time Analysis.
# 
#     4.1 How was the growth of Subscribers over Time on Udemy?
#     
#     4.2 What was the year that had the most subsribers?

# In[27]:


def calculate_popular_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes in a dataframe and calculates the number of courses 
    in each category and subcategory.
    """
    # Calculate the total number of courses within each category and subcategory
    category_counts = df.groupby(["category", "subcategory"]).size()                         .reset_index(name="count")

    # Sort the groups by the count in descending order
    return category_counts.sort_values(by="count", ascending=False)                           .reset_index(drop=True)


# ## 1.What is the most popular categories and subcategories?

# In[28]:


# Calculating the most popular categories
most_popular_categories = calculate_popular_categories(df1)


# In[29]:


most_popular_categories.head()


# In[30]:


# sorting the size column 
top_category =most_popular_categories.drop_duplicates("category")[:5]


# In[31]:


top_category.head()


# In[32]:


top_5_category=top_category.head()


# In[33]:


fig= px.bar(top_5_category[::-1],x="count",y='category',text_auto='.5s',orientation='h',
            color_discrete_sequence=px.colors.qualitative.Pastel
            ,title="Top 5 most popular udemy course Category")
fig.show()


# In[34]:


top_5_subcategory=top_category[["subcategory","count"]].head()


# In[35]:


top_5_subcategory= top_category[['subcategory','count']].drop_duplicates('subcategory')[:5]


# In[36]:


fig= px.bar(top_5_subcategory[::-1],x="count",y='subcategory',text_auto='.5s',orientation='h',
            color_discrete_sequence=px.colors.qualitative.Pastel
            ,title="Top 5 most popular Subcategory wise courses count")
fig.show()


# ## 1.1. What is the most Popular Course in each category?

# In[37]:


def find_most_popular_courses(df1,popularity_metric="num_subscribers",top_n=1):
    
    
    sorted_data=df1.sort_values(by=popularity_metric,ascending=False).groupby('category')
    
    
    return sorted_data.head(top_n)
    


# In[38]:


most_popular_courses= find_most_popular_courses(df1)
most_popular_courses[["title","category",'num_subscribers']].reset_index(drop=True)                    .sort_values('num_subscribers',ascending=False)


# In[39]:


# Showing the most popular courses and their "title", "category" and "num_subscribers"
most_popular_courses[["title","category", "num_subscribers"]].reset_index(drop=True)                                                                 .sort_values("num_subscribers",
                                                                             ascending=False)


# ## 2.  Pricing Analysis

# ### 2.1  Price distribution of courses

# In[40]:


courses_price = df1[df1["price"]>0]


# In[41]:


fig = px.histogram(data_frame=courses_price,x="price",nbins=50,
                  title="Distribution of courses price")
fig.show()


# ### The bulk of courses cost less than 200 dollars, with a sizeable number of them being provided for free. After spending more than 200 dollars, the number of courses significantly drops off, with only a few courses remaining in the distribution at 800 dollars and 1000 dollars.

# # Most of the courses are below $200  

# In[42]:


# courses according to prices

# courses below $200
below_200=len(df1[df1["price"]<200])

# courses above $200
above_200 =len(df1[df1["price"]>=200])


#calculating  total precentage

total_count = below_200 +above_200

# calculating % of courses price below and above $200
below_200_percentage = round((below_200/total_count)*100,2)
above_200_percentage = round((above_200/total_count)*100,2)

# creating dataframe forr percentage

percentage=pd.DataFrame({"price_range":["below_$200" ,"above_$200"],
                            "percentage":[below_200_percentage ,above_200_percentage],
                            "counts":[below_200,above_200]})


# ## 2.2. What is the percetange of courses that are priced below 200$ on udemy?

# ## Percentage of courses that are priced  below $200 on udemy 

# In[43]:


percentage


# In[44]:


# ploting pie chart for better visualization
fig =px.pie(data_frame=percentage ,names="price_range",values="percentage",color='price_range',
            hover_data="counts",
           title="Course distribution below and above $200",hole=0.70,
          color_discrete_map={'below_$200':"#687EFF",
                              'above_$200': "#B6FFFA"})
fig.show()


# ## 3. Instructor Performance

#  ## 3.1  Top 5 instructor with highest numbers of subscribers on Udemy 

# In[45]:


instructor_subscriber_counts=df1.groupby('instructor_name')['num_subscribers'].sum().reset_index()


# In[46]:


instructor_subscriber_counts = instructor_subscriber_counts.sort_values('num_subscribers',ascending=False)


# In[47]:


instructor_subscriber_counts = instructor_subscriber_counts.reset_index()


# In[48]:


instructor_subscriber_counts.head()


# In[49]:


# top 5 most performing instructors according to the number of subscribers


fig=px.bar(data_frame=instructor_subscriber_counts[:5],x='instructor_name' ,y='num_subscribers',
          text_auto='.5s',orientation='v',
            color_discrete_sequence=px.colors.qualitative.Pastel
            ,title="Top 5 most performing instructors according to the number of subscribers")

fig.show()


# ## Top most experienced instructor in terms of courses published on Udemy

# In[50]:


# Top most experienced instructors in terms of (courses published on udemy)

# grouping  dataframe by instructors name and  calculating number of courses taught by each instructors
experience= df1.groupby(["instructor_name"])["id"].count().reset_index()


# In[51]:


experience.rename(columns={"id":"num_courses"} ,inplace=True)


# In[52]:


experience


# In[53]:


experience = experience.sort_values("num_courses",ascending=False)


# In[54]:


# top 5 instructors name having most number of courses
top_5_instructor = experience.reset_index(drop=True)[:5]


# In[55]:


top_5_instructor


# ## 4.Time Analysis

# ## Growth of subcribers on Udemy over a time

# In[56]:


df_time=df1.set_index("published_time")


# In[57]:


monthly_subscriber_growth=df_time["num_subscribers"].resample("M").sum()


# In[58]:


monthly_subscriber_growth


# In[59]:


fig = px.line(monthly_subscriber_growth ,x=monthly_subscriber_growth.index,
              y=monthly_subscriber_growth.values,
             title="Subscriber growth over time",)
fig.show()


# ### Analysing the subscriber growth path suggests a steady increasing trajectory beginning in early 2013, reaching a high in 2020, and then beginning to see a major fall in early 2021. This finding reveals a significant upward trend in subscriber numbers throughout time, followed by a large downward trend in the most recent time frame.
# 
# ### Due to Covid-19 Pandamic, the subscription trajectory increased between 2020 and 2021. 

# In[60]:


# Year that had most number of subcribers

df1_year = df1.copy()
df1_year["Year"] = df1_year["published_time"].dt.year


# In[61]:


# yealy sybscribers

yearly_subscribers =df1_year.groupby('Year')["num_subscribers"].sum().reset_index()


# In[62]:


max(yearly_subscribers["num_subscribers"])


# In[63]:



fig = px.bar(yearly_subscribers, x='Year', y="num_subscribers", text_auto='.3s', color="num_subscribers",
            title= "Yearly Subscriber Growth ")
fig.update_layout(barmode='stack',
                 title_x=0.5)
fig.show()


# ## Courses launched in each year

# In[64]:


# number of courses by year
yearly_courses = df1_year.groupby("Year")["id"].count().reset_index()

yearly_courses.rename(columns={"id":"num_courses"},inplace=True)


# In[65]:


# Creating bar chart visualization for better understanding

fig = px.bar(yearly_courses, x='Year', y="num_courses", text_auto='.3s', color="num_courses",
            title= "Yearly Subscriber Growth ")
fig.update_layout(barmode='stack',
                 title_x=0.5)
fig.show()


# In[ ]:





# In[66]:


fig=px.histogram(data_frame=df1,x="language" ,text_auto=".3f",color="language")
fig.show()


# In[67]:


a=(df1[df1["language"]=="English"]).shape[0]


# In[68]:


(a/df1.shape[0])*100


# ### 59 % of courses offered on udemy platform are in english language  and rest of courses are in other language

# ## Inferences
# 
# 
# 
# 
# - The Udemy Courses Comments dataset analysis reveals important findings. As popular course categories, IT & Software, Development, Teaching & Academics, Personal Development, and Business have evolved. Other IT & Web Development, IT Certifications, Language Learning, and Programming Languages are some of the subcategories that have seen growth.
# 
# - The Development category's "Java Tutorial for Complete Beginners" course received the most subscribers (1,752,367).
# 
# 
# 
# - Nearly 94.4% of courses cost less than $200, demonstrating affordability and accessibility. According to subscription numbers, Learn Tech Plus, TJ Walker, Phil Ebiner, YouAccel Tanning, and Star-Tech Academy are the top teachers.
# 
# 
# 
# - In terms of experience, the most courses were released by Packet Publishing, Bluelime Learning Solutions, lllumeo Learning, Laurence Svekis, and Infinite Skills.
# 
# - The temporal study shows steady subscriber growth that peaks in 2020 and then starts to decline in early 2021. With over 120,730,813 members, 2020 was notable for having the most users.
# 
# - These results indicate how widely used online education is, how diverse the course categories are, and how cost, teacher effectiveness, and temporal patterns affect user involvement.
# 
# - These findings offer useful information to Udemy and its stakeholders, highlighting the platform's role in promoting affordable education and a vibrant online learning community.
# 

# In[ ]:




