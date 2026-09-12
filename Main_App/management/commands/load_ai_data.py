import os
import pandas as pd
from django.core.management.base import BaseCommand
from Main_App.models import IntentMaster, FraudRiskRule, LeadScoringRule  # Change 'your_app_name' to your actual app name!

class Command(BaseCommand):
    help = 'Loads EstateFlow AI training data from the Excel dataset.'

    def handle(self, *args, **kwargs):
        # Ensure pandas can find the file in your project root
        file_path = os.path.join(os.getcwd(), 'EstateFlow_AI_Intent_Training_Dataset.xlsx')
        
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        xls = pd.ExcelFile(file_path)
        
        # 1. Load Intent Master (header=None because the sheet lacks headers)
        self.stdout.write("Loading Intent_Master...")
        df_intent = pd.read_excel(xls, 'Intent_Master', header=None)
        
        for _, row in df_intent.iterrows():
            # Skip empty rows if any exist
            if pd.isna(row[0]): 
                continue
                
            IntentMaster.objects.update_or_create(
                intent_id=str(row[0]).strip(),
                defaults={
                    'category': str(row[1]).strip() if pd.notna(row[1]) else '',
                    'intent_name': str(row[2]).strip() if pd.notna(row[2]) else '',
                    'customer_type': str(row[3]).strip() if pd.notna(row[3]) else '',
                    'example_utterance': str(row[4]).strip() if pd.notna(row[4]) else '',
                    'ai_logic_description': str(row[5]).strip() if pd.notna(row[5]) else '',
                    'next_best_action': str(row[6]).strip() if pd.notna(row[6]) else '',
                    'lead_classification': str(row[7]).strip() if pd.notna(row[7]) else '',
                    'base_score': int(row[8]) if pd.notna(row[8]) else 0,
                    'entities_to_extract': str(row[9]).strip() if pd.notna(row[9]) else '',
                    'requires_rm': str(row[10]).strip() if pd.notna(row[10]) else '',
                    'risk_level': str(row[11]).strip() if pd.notna(row[11]) else '',
                    'clarification_prompt': str(row[12]).strip() if pd.notna(row[12]) else '',
                    'notes': str(row[13]).strip() if pd.notna(row[13]) else ''
                }
            )

        # 2. Load Fraud Risk Rules (header=0 because it has headers)
        self.stdout.write("Loading Fraud_Risk_Rules...")
        df_fraud = pd.read_excel(xls, 'Fraud_Risk_Rules', header=0)
        
        for _, row in df_fraud.iterrows():
            if pd.isna(row['Risk_ID']):
                continue
                
            FraudRiskRule.objects.update_or_create(
                risk_id=str(row['Risk_ID']).strip(),
                defaults={
                    'signal': str(row['Signal']).strip() if pd.notna(row['Signal']) else '',
                    'example': str(row['Example']).strip() if pd.notna(row['Example']) else '',
                    'risk_level': str(row['Risk_Level']).strip() if pd.notna(row['Risk_Level']) else '',
                    'ai_action': str(row['AI_Action']).strip() if pd.notna(row['AI_Action']) else '',
                    'human_action': str(row['Human_Action']).strip() if pd.notna(row['Human_Action']) else '',
                    'data_to_log': str(row['Data_to_Log']).strip() if pd.notna(row['Data_to_Log']) else ''
                }
            )

        # 3. Load Lead Scoring Rules (header=0)
        self.stdout.write("Loading Lead_Scoring_Rules...")
        df_scoring = pd.read_excel(xls, 'Lead_Scoring_Rules', header=0)
        
        for _, row in df_scoring.iterrows():
            if pd.isna(row['Rule_ID']):
                continue
                
            LeadScoringRule.objects.update_or_create(
                rule_id=str(row['Rule_ID']).strip(),
                defaults={
                    'signal': str(row['Signal']).strip() if pd.notna(row['Signal']) else '',
                    'example': str(row['Example']).strip() if pd.notna(row['Example']) else '',
                    'points': int(row['Points']) if pd.notna(row['Points']) else 0,
                    'classification_impact': str(row['Classification_Impact']).strip() if pd.notna(row['Classification_Impact']) else '',
                    'notes': str(row['Notes']).strip() if pd.notna(row['Notes']) else ''
                }
            )

        self.stdout.write(self.style.SUCCESS("All AI rules successfully loaded into the database!"))