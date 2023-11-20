import sys
# print(sys.path)
sys.path.append('/home/star/projects/chat_doc')
from server.knowledge_base.kb_service.faiss_kb_service import FaissKBService
from server.knowledge_base.kb_service.milvus_kb_service import MilvusKBService
from server.knowledge_base.kb_service.pg_kb_service import PGKBService
from server.knowledge_base.kb_service.es_kb_service import ESKBService
from server.knowledge_base.kb_service.zilliz_kb_service import ZillizKBService
from server.knowledge_base.migrate import create_tables
from server.knowledge_base.utils import KnowledgeFile
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "7"
kbService = FaissKBService("lb_test")
test_kb_name = "lb_test"
test_file_name = "陕汽-新M3000S维修手册 第二部分.pdf"
testKnowledgeFile = KnowledgeFile(test_file_name, test_kb_name)
search_content = "驱动车桥的速比数据表"


def test_init():
    create_tables()


def test_create_db(kbService):
    assert kbService.create_kb()


def test_add_doc(kbService, testKnowledgeFile):
    assert kbService.add_doc(testKnowledgeFile)


def test_search_db(kbService):
    result = kbService.search_docs(search_content)
    # result = kbService.do_search(search_content, 3, 0.5)
    assert len(result) > 0
    return result
def test_delete_doc():
    assert kbService.delete_doc(testKnowledgeFile)


def test_update_doc():
    assert kbService.update_doc()


def test_delete_db(kbService):
    assert kbService.drop_kb()

import json
with open("/home/star/projects/chat_doc/tests/kb_vector_db/query.json", "r") as f:
    queries = json.load(f)

d = list()


# faiss的swigfaiss的indexflat.search是向量的L2距离和余弦距离
test_kb_name = "lb_test"
kbService = FaissKBService(test_kb_name)
# test_delete_db(kbService)
# test_create_db(kbService)
test_add_doc(kbService, testKnowledgeFile)

retrival_list = test_search_db(kbService)
for query, index in queries.items(): 
    answer_list = []
    search_content = query
    answers = test_search_db(kbService)
    # print(answers)
    # break
    for i in range(1):
        answer_list.append([i, answers[i][0].page_content[:100]])
    source = answers[0][0].metadata['source']
    length = len(answers[0][0].page_content)
    d.append({"page":index, 
              "query": query,
              "answer":answer_list,
              "source":source,
              "len":length})
              
with open("/home/star/projects/chat_doc/tests/kb_vector_db/answer.json", "w", encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=4)
# retrival_list[i][1]是相似度分数, retrival_list[i][0].page_content是文本, retrival_list[i][0].metadata['source']是source

print("=============================================================================================")

# test_kb_name = "test1"
# kbService = ESKBService(test_kb_name)
# test_create_db(kbService)
# test_add_doc(kbService, testKnowledgeFile)
# print(test_search_db(kbService))
# print("=============================================================================================")
# from server.db.base import Base, engine
# Base.metadata.create_all(bind=engine)
# test_kb_name = "test2"
# kbService = ZillizKBService(test_kb_name)
# test_create_db(kbService)
# test_add_doc(kbService, testKnowledgeFile)
# print(test_search_db(kbService))
# print("=============================================================================================")

# test_kb_name = "test3"
# kbService = PGKBService(test_kb_name)
# test_create_db(kbService)
# test_add_doc(kbService, testKnowledgeFile)
# print(test_search_db(kbService)) # 针对PostgreSQL
# print("=============================================================================================")

# test_kb_name = "test4"
# kbService = MilvusKBService(test_kb_name)
# test_create_db(kbService)
# test_add_doc(kbService, testKnowledgeFile)
# print(test_search_db(kbService)) # 大规模数据库，扩展性强
# print("=============================================================================================")