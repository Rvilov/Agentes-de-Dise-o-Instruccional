#!/usr/bin/env python3
"""v1.5 optimization regressions: synthetic fixtures, never real stock/fidelity signoff."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TESTS=ROOT/'tests'
sys.path.insert(0,str(TESTS))
sys.path.insert(0,str(ROOT/'shared/scripts'))
import test_v141_fidelity as baseline
write_json=baseline.write_json
digest=baseline.digest
from verify_review_passes import verify as verify_passes
from validate_content_qa_source import audit_fast, audit
from select_content_qa_controls import select

TIMES=['2026-10-27T12:00:00+00:00','2026-10-27T12:10:00+00:00',
       '2026-10-27T12:20:00+00:00','2026-10-27T12:30:00+00:00']
STAGES={'learning':['pedagogical-reviewer','dynamism-reviewer','accessibility-reviewer'],
        'editorial':['visual-stock-reviewer','template-format-reviewer','language-humanizer'],
        'fidelity':['source-fidelity-reviewer']}

class OptimizedReviewTests(unittest.TestCase):
    def setUp(self):
        self.fixture=baseline.FidelityRegressions('test_valid_document_claims_approved')
        self.fixture.setUp()
        self.root=self.fixture.root
        f=self.fixture
        # Fixture semantic review timestamp must postdate editorial and course consistency.
        review=json.loads(f.review.read_text())
        review['reviewed_at']=TIMES[3]
        write_json(f.review,review)
        write_json(self.root/'qa/course-resource-index.json',{'schema_version':'1.4.1','resources':[{'id':'R1','docx':'outputs/R1.docx'}]})
        self.consistency={'status':'VERDE','completed_at':TIMES[2],
            'resources':[{'id':'R1','docx':'outputs/R1.docx','sha256':digest(f.word)}],
            'issues':[],'review_notes':'Same client terminology and consistent requirements.'}
        write_json(self.root/'qa/course-consistency-review.json',self.consistency)
        self.rpt={}
        reg=json.loads((ROOT/'shared/references/content-qa-control-register.json').read_text())
        self.checks={c['id']:c for c in reg['controls']}
        self.build_reports()
    def tearDown(self):self.fixture.tearDown()

    def build_reports(self):
        available={a:(st,i) for st,roles in STAGES.items() for i,a in enumerate(roles)}
        self.rpt={}
        for idx,(phase,roles) in enumerate(STAGES.items()):
            reviews=[]
            for name in roles:
                record={'agent':name,'resource_id':'R1','status':'VERDE','issues':[],'content_qa_checks':[]}
                if name=='source-fidelity-reviewer':record['decision']='APROBADO'
                reviews.append(record)
            self.rpt[phase]={'pass':phase,'resource_id':'R1','completed_at':TIMES[idx if idx<2 else 3], 'reviews':reviews}
        for code,c in self.checks.items():
            reviewers=[x for x in c['agents'] if x in available]
            self.assertTrue(reviewers,code)
            name=reviewers[0]
            phase,j=available[name]
            self.rpt[phase]['reviews'][j]['content_qa_checks'].append(
                {'id':code,'result':'CUMPLE','evidence':'Evidencia solo sintetica de prueba; no es una certificacion real.','slides':c['source_slides']})
        for phase,doc in self.rpt.items():write_json(self.root/'qa'/('R1.pass-'+phase+'.json'),doc)

    def payload(self):return [self.rpt[x] for x in ('learning','editorial','fidelity')]
    def errors(self):return verify_passes(self.root,'R1',self.payload(),self.fixture.word)['errors']
    def aggregator(self):
        proc=subprocess.run([sys.executable,str(ROOT/'skills/final-qa/scripts/aggregate_reports.py'),
            *(str(self.root/'qa'/('R1.pass-'+p+'.json')) for p in ('learning','editorial','fidelity')),
            '--project-dir',str(self.root),'--resource-id','R1','--docx','outputs/R1.docx',
            '--enforce-three-passes','--compact'],capture_output=True,text=True)
        return proc.returncode,json.loads(proc.stdout)

    def test_all_three_passes_accepted_with_fresh_fidelity(self):
        self.assertEqual([],self.errors())
        code,result=self.aggregator()
        self.assertEqual(code,0,result)
        self.assertEqual(result['status'],'VERDE')

    def test_missing_learning_agent_blocks(self):
        self.rpt['learning']['reviews'].pop()
        self.assertIn('REVIEW_PASS_AGENTS_INCOMPLETE',' '.join(self.errors()))

    def test_wrong_review_order_blocks(self):
        self.rpt['fidelity']['completed_at']=TIMES[0]
        self.assertIn('REVIEW_PASS_ORDER_INVALID',' '.join(self.errors()))

    def test_course_consistency_not_completed_blocks(self):
        (self.root/'qa/course-consistency-review.json').unlink()
        self.assertIn('COURSE_CONSISTENCY_REVIEW_MISSING',' '.join(self.errors()))

    def test_final_word_change_blocks_fidelity_and_consistency(self):
        from docx import Document
        d=Document(self.fixture.word)
        d.tables[-1].rows[1].cells[1].text+=' Fastest approval in the world.'
        d.save(self.fixture.word)
        self.assertIn('COURSE_CONSISTENCY_STALE_WORD',' '.join(self.errors()))
        self.assertEqual(self.aggregator()[1]['status'],'ROJO')

    def test_reviewed_at_before_editorial_blocks(self):
        report=json.loads(self.fixture.review.read_text());report['reviewed_at']=TIMES[0]
        write_json(self.fixture.review,report)
        self.assertIn('FIDELITY_SEMANTIC_REVIEW_BEFORE_EDITORIAL',' '.join(self.errors()))

    def test_no_registered_source_quote_still_blocks(self):
        self.fixture.rewrite(self.fixture.ledger, lambda d:d['claims'][0]['evidence'][0].update({'quote':'Only fictional evidence'}))
        self.assertEqual(self.aggregator()[1]['status'],'ROJO')

    def test_27_controls_wrong_agent_blocks(self):
        self.rpt['editorial']['reviews'][2]['content_qa_checks'].append(
           {'id':'CQ-01','result':'CUMPLE','evidence':'Wrong reviewer intentionally','slides':[4]})
        write_json(self.root/'qa/R1.pass-editorial.json',self.rpt['editorial'])
        code,result=self.aggregator()
        self.assertNotEqual(code,0)
        self.assertEqual(result['status'],'ROJO')

    def test_control_register_select_only_relevant(self):
        items=select(ROOT/'shared',['pedagogical-reviewer'])
        self.assertGreater(len(items),0)
        self.assertLess(len(items),27)
        self.assertTrue(all('id' in x and 'slides' in x for x in items))

    def test_fast_and_full_QA_integrity(self):
        self.assertEqual(audit_fast(ROOT/'shared')['status'],'OK')
        self.assertEqual(audit(ROOT/'shared')['status'],'OK')

    def test_draft_gate_skips_factual_fidelity_without_integral_green(self):
        project=self.root
        # No installed special agents, other gates correctly fail, but fidelity not invoked during drafting.
        proc=subprocess.run([sys.executable,str(ROOT/'shared/scripts/run_quality_gates.py'),
            '--project-dir',str(project),'--resource-id','R1','--docx','outputs/R1.docx',
            '--phase','draft','--compact','--report','qa/R1.draft.json'],capture_output=True,text=True)
        report=json.loads((project/'qa/R1.draft.json').read_text())
        self.assertEqual(report['phase'],'draft')
        self.assertNotIn('factual_fidelity',[v['gate'] for v in report['gates']])
        self.assertFalse(report['integral_release_eligible'])
        self.assertIn('pass',json.loads(proc.stdout))

if __name__=='__main__':unittest.main()
