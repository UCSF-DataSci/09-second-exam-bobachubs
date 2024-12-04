from scipy import stats
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf 
from sklearn.preprocessing import OrdinalEncoder
import seaborn as sns

## Question 3: Statistical Analysis (25 points)

# Perform statistical analysis on both outcomes:

# 1. Analyze walking speed:
#    - Multiple regression with education and age
#    - Account for repeated measures
#    - Test for significant trends

# 2. Analyze costs:
#    - Simple analysis of insurance type effect
#    - Box plots and basic statistics
#    - Calculate effect sizes

# 3. Advanced analysis:
#    - Education age interaction effects on walking speed
#    - Control for relevant confounders
#    - Report key statistics and p-values

# Tips:

# - Use scipy.stats for statistical tests
# - Use statsmodels for regression analysis:
#   - Report coefficients and confidence intervals

df = pd.read_csv('test.csv')

#1. linear mixed effects model for multiple data for a single patient

#  age has no outliers and is relatively normal
# plt.figure(figsize=(10, 6))
# plt.boxplot(df['age'])
# plt.hist(df['age'])
# plt.title('age')
# plt.show()

# walking speed has a few positive outliers but is relatively normal
# plt.figure(figsize=(10, 6))
# plt.boxplot(df['walking_speed'])
# plt.hist(df['walking_speed'])
# plt.title('walking speed')
# plt.show()

# get rid of outliers for walking speed
z_scores = np.abs(stats.zscore(df['walking_speed']))
df = df[(z_scores < 3)]

# OR...
# Q1 = df['column'].quantile(0.25)
# Q3 = df['column'].quantile(0.75)
# IQR = Q3 - Q1
# df_clean = df[~((df['column'] < (Q1 - 1.5 * IQR)) | (df['column'] > (Q3 + 1.5 * IQR)))]


full_model = smf.mixedlm("walking_speed ~ education_level + age", 
                          data=df, 
                          groups=df["patient_id"]).fit()

print(full_model.summary()) 
#coefficients are all significant, the model seem so to be very significant with narrow CIs

# ----------------------------------------------------------------------------
#                                 Coef.  Std.Err.    z     P>|z| [0.025 0.975]
# ----------------------------------------------------------------------------
# Intercept                        5.603    0.011  497.434 0.000  5.581  5.625
# education_level[T.Graduate]      0.402    0.009   45.546 0.000  0.385  0.419
# education_level[T.High School]  -0.788    0.009  -92.005 0.000 -0.805 -0.772
# education_level[T.Some College] -0.406    0.009  -46.868 0.000 -0.423 -0.389
# age                             -0.030    0.000 -166.796 0.000 -0.030 -0.030

# visual trend analysis for age and walking speed
print("\nTrend Analysis:")
sns.scatterplot(data=df, x='age', y='walking_speed', hue='education_level', alpha=0.6, s=25)
plt.title("Walking Speed by Age and Education Level")
# plt.savefig('trend_analysis.png')
# there are clear clusters of age vs walking speed by the education level

# testing significance between age and walking speed alone
trend_test = stats.linregress(df['age'], df['walking_speed'])
# print(trend_test)
print(f"Trend p-value: {trend_test.pvalue}") #0.0
# p-value is low and this simple linear regression is significant


# doing a LRT to determine if adding education improves the model 
reduced_model = smf.mixedlm("walking_speed ~ age", data=df, groups=df["patient_id"]).fit(reml=False)
lr_stat = 2 * (full_model.llf - reduced_model.llf)
p_value = stats.chi2.sf(lr_stat, df=1)
print(f"Likelihood Ratio Test Statistic: {lr_stat}") #3235.32
print(f"P-value: {p_value}") #p=0.0
# yes the p-value is very low so the linear mixed effects with both age and education is very significant


#2.
# the costs are pretty uniformally/normally distributed across the insurance types, health insurance has a higher range
plt.figure(figsize=(10, 6))
df.groupby('insurance_type')['visit_cost'].hist(alpha=0.5, legend=True)
plt.title('Cost Distribution by Insurance Type')
# plt.savefig('insurance_cost_distribution.png')

# One-way ANOVA to test insurance type effect
insurance_groups = [group['visit_cost'].values for _, group in df.groupby('insurance_type')]
f_statistic, p_value = stats.f_oneway(*insurance_groups)
print('One-way ANOVA test to determine insurance type effect')
print('f_statistic', f_statistic) #21017.93
print('p-value', p_value) #0.0
print("visit cost descriptions by insurance type")
# print(df.groupby('insurance_type')['visit_cost'].describe())
# calculate effect size or eta^2
eta_squared = f_statistic * (len(insurance_groups) - 1) / (f_statistic * (len(insurance_groups) - 1) + sum(len(g) for g in insurance_groups))
print("eta-squared: ", eta_squared)  #.89

#3
# trend analysis for interaction between education level and age
# insurance may be a confounder
print("\ntesting interaction")
df['education_numeric'] = OrdinalEncoder().fit_transform(df[['education_level']])
trend_model = smf.ols("walking_speed ~ education_numeric * age", data=df).fit()
print("\nEducation-Age Interaction Trend Analysis:")
print('R^2: ', 0.595)
print('Pr(F-stat = 7521): ', 0.0)
print(trend_model.summary())
# walking speed tends to decrease with age and slightly with education level (negative correlations)
# education is inconsistent with age for different walking speeds (barely any interaction), the coefficients are similar to the crude

# testing if insurance is a potential confounder
# df['insurance_numeric'] = OrdinalEncoder().fit_transform(df[['insurance_type']])
# trend_model = smf.ols("walking_speed ~ education_numeric * age + insurance_numeric", data=df).fit()
# print("\nEducation-Age Interaction Trend Analysis:")
# print(trend_model.summary())
# it is not since the coefficient remained about the same