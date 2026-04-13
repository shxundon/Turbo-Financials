"""
Utility script for managing Turbo Financials form submissions
Provides tools for viewing, exporting, and analyzing logged data
"""

import json
import csv
from pathlib import Path
from datetime import datetime
import argparse


class SubmissionManager:
    def __init__(self, data_dir='logs/submissions'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def get_all_submissions(self, form_type=None):
        """Get all submissions, optionally filtered by type"""
        submissions = []
        for file in sorted(self.data_dir.glob('*.json'), reverse=True):
            if form_type and form_type not in str(file):
                continue
            try:
                with open(file) as f:
                    submissions.append(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {file}")
        return submissions
    
    def print_summary(self):
        """Print summary of all submissions"""
        submissions = self.get_all_submissions()
        
        tax_count = len([s for s in submissions if 'tax_information' in s['form_type']])
        bank_count = len([s for s in submissions if 'bank_information' in s['form_type']])
        dd_count = len([s for s in submissions if 'direct_deposit' in s['form_type']])
        
        print("\n" + "="*50)
        print("SUBMISSION SUMMARY")
        print("="*50)
        print(f"Total Submissions:      {len(submissions)}")
        print(f"Tax Information:        {tax_count}")
        print(f"Bank Information:       {bank_count}")
        print(f"Direct Deposit:         {dd_count}")
        
        if submissions:
            print(f"\nFirst Submission:       {submissions[-1]['timestamp']}")
            print(f"Last Submission:        {submissions[0]['timestamp']}")
        print("="*50 + "\n")
    
    def print_recent(self, limit=5):
        """Print recent submissions"""
        submissions = self.get_all_submissions()[:limit]
        
        print(f"\nRecent {limit} Submissions:")
        print("-" * 50)
        
        for sub in submissions:
            timestamp = sub['timestamp']
            form_type = sub['form_type'].replace('_', ' ').title()
            
            if 'full_name' in sub['data']:
                name = sub['data']['full_name']
            elif 'account_holder_name' in sub['data']:
                name = sub['data']['account_holder_name']
            elif 'employee_name' in sub['data']:
                name = sub['data']['employee_name']
            else:
                name = "Unknown"
            
            print(f"[{timestamp}] {form_type}: {name}")
        print("-" * 50 + "\n")
    
    def export_to_csv(self, form_type=None, output_file=None):
        """Export submissions to CSV"""
        submissions = self.get_all_submissions(form_type)
        
        if not submissions:
            print("No submissions to export")
            return
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            form_suffix = f"_{form_type}" if form_type else ""
            output_file = f"export{form_suffix}_{timestamp}.csv"
        
        # Flatten all data
        rows = []
        for sub in submissions:
            row = {
                'timestamp': sub['timestamp'],
                'form_type': sub['form_type']
            }
            row.update(sub['data'])
            rows.append(row)
        
        # Get all unique field names
        fieldnames = set()
        for row in rows:
            fieldnames.update(row.keys())
        fieldnames = sorted(list(fieldnames))
        
        # Write CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✓ Exported {len(rows)} submissions to: {output_file}")
    
    def export_to_json(self, form_type=None, output_file=None):
        """Export submissions to JSON file"""
        submissions = self.get_all_submissions(form_type)
        
        if not submissions:
            print("No submissions to export")
            return
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            form_suffix = f"_{form_type}" if form_type else ""
            output_file = f"export{form_suffix}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, indent=2)
        
        print(f"✓ Exported {len(submissions)} submissions to: {output_file}")
    
    def delete_old_submissions(self, days=30):
        """Delete submissions older than specified days"""
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        for file in self.data_dir.glob('*.json'):
            try:
                with open(file) as f:
                    data = json.load(f)
                    timestamp = datetime.fromisoformat(data['timestamp'])
                    
                    if timestamp < cutoff:
                        file.unlink()
                        deleted_count += 1
            except (json.JSONDecodeError, KeyError):
                pass
        
        print(f"✓ Deleted {deleted_count} submissions older than {days} days")
    
    def view_submission(self, index):
        """View a specific submission"""
        submissions = self.get_all_submissions()
        
        if index < 0 or index >= len(submissions):
            print(f"Invalid index: {index}")
            return
        
        sub = submissions[index]
        print("\n" + "="*60)
        print(f"SUBMISSION #{index + 1}")
        print("="*60)
        print(json.dumps(sub, indent=2))
        print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Turbo Financials Submission Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python manage.py summary              # View submission summary
  python manage.py recent               # View 5 most recent
  python manage.py recent -n 10         # View 10 most recent
  python manage.py export --csv         # Export to CSV
  python manage.py export --json        # Export to JSON
  python manage.py export --csv --type tax_information
  python manage.py view 0               # View first submission
  python manage.py delete-old --days 30 # Delete submissions > 30 days old
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Summary command
    subparsers.add_parser('summary', help='View submission summary')
    
    # Recent command
    recent_parser = subparsers.add_parser('recent', help='View recent submissions')
    recent_parser.add_argument('-n', '--number', type=int, default=5, help='Number of recent submissions to show')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export submissions')
    export_parser.add_argument('--csv', action='store_true', help='Export to CSV')
    export_parser.add_argument('--json', action='store_true', help='Export to JSON')
    export_parser.add_argument('--type', help='Filter by form type')
    export_parser.add_argument('--output', help='Output filename')
    
    # View command
    view_parser = subparsers.add_parser('view', help='View specific submission')
    view_parser.add_argument('index', type=int, help='Submission index (0-based)')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete-old', help='Delete old submissions')
    delete_parser.add_argument('--days', type=int, default=30, help='Delete submissions older than N days')
    
    args = parser.parse_args()
    
    manager = SubmissionManager()
    
    if args.command == 'summary':
        manager.print_summary()
    
    elif args.command == 'recent':
        manager.print_recent(args.number)
    
    elif args.command == 'export':
        if args.csv:
            manager.export_to_csv(args.type, args.output)
        elif args.json:
            manager.export_to_json(args.type, args.output)
        else:
            print("Please specify --csv or --json")
    
    elif args.command == 'view':
        manager.view_submission(args.index)
    
    elif args.command == 'delete-old':
        manager.delete_old_submissions(args.days)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
