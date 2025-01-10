from utils import load_fixtures, completed_fixtures
import pandas as pd

if __name__ == '__main__':
    df = load_fixtures()
    print('Saving to fixtures_and_schedules')
    df.to_csv('fixture_list/fixtures_and_schedule.csv', index = False)
    completed = completed_fixtures(df)
    print('Saving completed fixtures')
    completed.to_csv('fixture_list/completed_fixtures.csv', index = False) 