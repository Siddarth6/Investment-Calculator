import streamlit as st
import plotly.graph_objects as go
import numpy as np
import numpy_financial as nf

st.set_page_config(page_title="Mini Project")
st.title("Mini Project: Financial planning")

tab1,tab2,tab3 = st.tabs(["Monthly Savings","EMI Calculator","Pay off vs Invest"])

with tab1:
    st.header("**Monthly Income**")
    st.subheader("Salary")
    colAnnualSal, colTax = st.columns(2)

    with colAnnualSal:
        salary = st.number_input("Enter your annual salary(₹): ",min_value=0.0,format='%f')
    with colTax:
        tax_rate = st.number_input("Enter your tax rate(%): ",min_value=0.0,format='%f')

    tax_rate=tax_rate/100.0
    salary_after_tax = salary*(1-tax_rate)
    monthly_takehome=round(salary_after_tax/12.0,2)
    rec_invest=str(round(0.2*monthly_takehome,2))

    st.header("**Monthly Expenses**")
    colExpenses1, colExpenses2 = st.columns(2)

    with colExpenses1:
        st.subheader("Rent")
        monthly_rental = st.number_input("Enter your monthly rental(₹): ", min_value=0.0,format='%f' )
    
        st.subheader("Daily Food Budget")
        daily_food = st.number_input("Enter your daily food budget (₹): ", min_value=0.0,format='%f' )
        monthly_food = daily_food * 30
    
        st.subheader("Unforeseen Expenses")
        monthly_unforeseen = st.number_input("Enter your monthly unforeseen expenses (₹): ", min_value=0.0,format='%f' ) 
    
    with colExpenses2:
        st.subheader("Transport")
        monthly_transport = st.number_input("Enter your monthly transport fee (₹): ", min_value=0.0,format='%f' )   
    
        st.subheader("Utilities Fees")
        monthly_utilities = st.number_input("Enter your monthly utilities fees (₹): ", min_value=0.0,format='%f' )
    
        st.subheader("Entertainment Budget")
        monthly_entertainment = st.number_input("Enter your monthly entertainment budget (₹): ", min_value=0.0,format='%f' )   

    monthly_expenses = monthly_rental + monthly_food + monthly_transport + monthly_entertainment + monthly_utilities + monthly_unforeseen
    monthly_savings = monthly_takehome - monthly_expenses 


    st.header("**Savings**")
    st.subheader("Monthly Take Home Salary: ₹" + str(round(monthly_takehome,2)))
    st.subheader("Monthly Expenses: ₹" + str(round(monthly_expenses, 2)))
    st.subheader("Monthly Savings: ₹" + str(round(monthly_savings, 2)))
    st.markdown("---")
    st.header("**Forecast Savings**")
    colForecast1, colForecast2 = st.columns(2)
    with colForecast1:
        st.subheader("Forecast Year")
        forecast_year = st.number_input("Enter your forecast year (Min 1 year): ", min_value=0,format='%d')
        forecast_months = 12 * forecast_year 
    
        st.subheader("Annual Inflation Rate")
        annual_inflation = st.number_input("Enter annual inflation rate (%): ", min_value=0.0,format='%f')
        monthly_inflation = (1+annual_inflation)**(1/12) - 1
        cumulative_inflation_forecast = np.cumprod(np.repeat(1 + monthly_inflation, forecast_months))
        forecast_expenses = monthly_expenses*cumulative_inflation_forecast
    with colForecast2:
        st.subheader("Annual Salary Growth Rate")
        annual_growth = st.number_input("Enter your expected annual salary growth (%): ", min_value=0.0,format='%f')
        monthly_growth = (1 + annual_growth) ** (1/12) - 1
        cumulative_salary_growth = np.cumprod(np.repeat(1 + monthly_growth, forecast_months))
        forecast_salary = monthly_takehome * cumulative_salary_growth 
    
    forecast_savings = forecast_salary - forecast_expenses 
    cumulative_savings = np.cumsum(forecast_savings)
    x_values = np.arange(forecast_year + 1)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_values, 
            y=forecast_salary,
            name="Forecast Salary"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=forecast_expenses,
            name= "Forecast Expenses"
        )
    )

    fig.add_trace(
        go.Scatter(
                x=x_values, 
                y=cumulative_savings,
                name= "Forecast Savings"
            )
    )
    fig.update_layout(title='Forecast Salary, Expenses & Savings Over the Years',
                   xaxis_title='Year',
                   yaxis_title='Amount($)')

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("**EMI Calculator**")
    colLA,colR = st.columns(2)
    colT,colPlace = st.columns(2)
    with colLA:
        LoanAmt = st.number_input("Enter your loan amount(₹): ",min_value=0,format="%d")
    with colR:
        rate = st.number_input("Enter rate of interest(%): ",min_value=0,format="%d")
    with colT:
        tenure = st.number_input("Enter your tenure period(Years): ",min_value=0,format="%d")
    if(tenure>0):
        emi=round(-nf.pmt((rate/100)/12,tenure*12,LoanAmt))
        intPaid=-(-nf.ipmt((rate/100)/12,tenure*12,1*12,LoanAmt))
        totalInt=round(LoanAmt+intPaid)
        st.subheader("Equated Monthly Instalment(EMI): ₹"+str(emi))
        st.subheader("Total interest paid: ₹"+str(totalInt))
   
with tab3:
    st.header("Should you pay off your loan or invest?")
    colLoan,colRate = st.columns(2)
    colMOL,colRM = st.columns(2)
    colLM,colM = st.columns(2)
    colGR, colPl = st.columns(2)

    with colLoan:
        loan = st.number_input("Enter loan amount(₹): ",min_value=0,format='%d')
    with colRate:
        r = st.number_input("Enter loan interest rate(%): ",min_value=0.0,format='%f')
    with colMOL:
        monthofLoan = st.number_input("Enter current month of loan(Months): ",min_value=0,format='%d')
    with colRM:
        remainMonth = st.number_input("Enter remaining months of of loan(Month): ",min_value=0,format='%d')
    with colLM:
        lumpSum = st.number_input("Enter lumpsum amount you have(₹): ",min_value=0,format='%d')
    with colM:
        monthlyInv = st.number_input("Enter monthly investment amount(₹): ",min_value=0,format='%d')
    with colGR:
        yearlyReturn = st.number_input("Enter returns you can generate every year(%): ",min_value=0.0,format='%f')
    totalI = -nf.ipmt((r/100)/12,(remainMonth+monthofLoan)/12,1*12,loan)
    pay=(round(totalI*(remainMonth-monthofLoan)))
    invested=(lumpSum+monthlyInv*remainMonth)
    grown=(round(-nf.fv((yearlyReturn/100)/12,remainMonth,monthlyInv,lumpSum)))
    made=grown-invested
    st.subheader("You will pay interest of: ₹"+str(pay))
    st.subheader("You would have invested: ₹"+str(invested))
    st.subheader("Your investment would have grown to: ₹"+str(grown))
    st.subheader("Your investment as made: ₹"+str(made))
    st.markdown("---")
    if(made>pay):
        st.header("**Invest your money**")
        st.subheader("Since growth of investment is more.")
    if(made<pay):
        st.header("**Pay off loan**")
        st.subheader("Since growth of investment is not enough")