import utils.linear_targets as linear_targets, utils.exponential_targets as exponential_targets

"""
Use this to make use of the script
"""


df = linear_targets.target_dataframe_gen(
        start_year = 2023,end_year = 2029,targets= {
    "pue_users_target": 16000,
    "private_investment_mobilied_target": 30000000,
    "satisfied_beneficiaries_target": 80,
    "women_owned_businesses_with_electricity_target": 10000,
    "women_headed_households_with_electricty_target": 16000,
    "female_stem_graduates_hired_in_energy_target": 80,
    "contractors_with_stakeholder_meetings_percentage_target": 90,
    "connections_via_distributed_renewable_energy_devices_target": 10000,
    "renewable_energy_capacity_enabled_target": 5
    }

)

# df.to_csv('testing_this_out.csv',index=False)

df1 = exponential_targets.target_dataframe_gen(
        start_year = 2024,end_year = 2031,targets= {
    "private_capital_mobilized": 5000000
    }
)
df1.to_csv('exp_results_capital.csv',index=False)