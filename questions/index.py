from questions.House_Type import House_Type_Question
from questions.Price_Correlation import Price_Correlation_Question
from questions.House_Price_Fluctuation import Price_Fluctuation_Question
from questions.District_Information import District_Information_Question
from utils.index import get_hash

def get_questions():
    questions = [  
        {
            "component": House_Type_Question,
            "name": "🏚 House Type",
            "icon": "front"
        },
        {
            "component": Price_Correlation_Question,
            "name": "💰 Price correlation",
            "icon": "cash-coin"
        },
        {
            "component": Price_Fluctuation_Question,
            "name": "📉 Price Fluctuation",
            "icon": "cash-coin"
        },
        {
            "component": District_Information_Question,
            "name": "🌆 District Information",
            "icon": "cash-coin"
        },
    ]
    
    return get_hash(questions)