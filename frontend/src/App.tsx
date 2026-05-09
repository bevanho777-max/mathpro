import { useEffect, useMemo, useState } from 'react';
import { InlineMath } from 'react-katex';

type KnowledgePoint = {
  id: string;
  name: string;
  semester: string;
};

type Problem = {
  problem_id: string;
  template_id: string;
  grade: string;
  semester: string;
  module: string;
  knowledge_point: string;
  difficulty: number;
  question_type: string;
  question: string;
  solution: string;
  parameters: Record<string, string | number>;
};

type CheckResult = {
  correct: boolean;
};

type WrongBookItem = {
  id: number;
  problem_id: string;
  template_id: string;
  grade: string;
  semester: string;
  module: string;
  knowledge_point: string;
  difficulty: number;
  question_type: string;
  question: string;
  solution: string;
  first_wrong_answer: string;
  last_wrong_answer: string;
  wrong_count: number;
  removed: boolean;
  created_at: string;
  last_wrong_at: string;
  removed_at: string | null;
};

type ViewMode = 'practice' | 'wrong-book';
type LoadState = 'idle' | 'loading' | 'ready' | 'error';

function apiUrl(path: string, params?: Record<string, string>) {
  const search = params ? `?${new URLSearchParams(params).toString()}` : '';
  return `${path}${search}`;
}

function friendlyApiMessage(message: string) {
  if (message.includes('No templates found')) {
    return '当前范围暂无题目，请换一个知识点或章节。';
  }
  return message || '请求失败，请稍后再试。';
}

async function readErrorMessage(response: Response) {
  const text = await response.text();
  if (!text) {
    return `HTTP ${response.status}`;
  }

  try {
    const payload = JSON.parse(text) as { detail?: unknown };
    if (typeof payload.detail === 'string') {
      return friendlyApiMessage(payload.detail);
    }
  } catch {
    return friendlyApiMessage(text);
  }

  return friendlyApiMessage(text);
}

async function fetchJson<T>(path: string, params?: Record<string, string>, init?: RequestInit): Promise<T> {
  const response = await fetch(apiUrl(path, params), init);
  if (!response.ok) {
    const message = await readErrorMessage(response);
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

function MathText({ text }: { text: string }) {
  const parts = text.split('$');

  return (
    <>
      {parts.map((part, index) => {
        const key = `${index}-${part}`;
        if (index % 2 === 1) {
          return <InlineMath key={key} math={part} />;
        }
        return <span key={key}>{part}</span>;
      })}
    </>
  );
}

export default function App() {
  const [viewMode, setViewMode] = useState<ViewMode>('practice');
  const [grades, setGrades] = useState<string[]>([]);
  const [modules, setModules] = useState<string[]>([]);
  const [knowledgePoints, setKnowledgePoints] = useState<KnowledgePoint[]>([]);

  const [grade, setGrade] = useState('');
  const [moduleName, setModuleName] = useState('');
  const [knowledgePoint, setKnowledgePoint] = useState('');

  const [problem, setProblem] = useState<Problem | null>(null);
  const [answer, setAnswer] = useState('');
  const [checkResult, setCheckResult] = useState<CheckResult | null>(null);
  const [showSolution, setShowSolution] = useState(false);

  const [loadState, setLoadState] = useState<LoadState>('idle');
  const [message, setMessage] = useState('');
  const [wrongBookItems, setWrongBookItems] = useState<WrongBookItem[]>([]);
  const [wrongBookLoading, setWrongBookLoading] = useState(false);
  const [wrongBookMessage, setWrongBookMessage] = useState('');

  const canLoadByKnowledge = Boolean(grade && moduleName && knowledgePoint);
  const hasPracticeScope = Boolean(moduleName && knowledgePoint);
  const selectedPoint = useMemo(
    () => knowledgePoints.find((item) => item.name === knowledgePoint),
    [knowledgePoint, knowledgePoints],
  );

  useEffect(() => {
    setLoadState('loading');
    fetchJson<string[]>('/api/grades')
      .then((items) => {
        setGrades(items);
        setGrade(items[0] ?? '');
        setLoadState('ready');
      })
      .catch((error: Error) => {
        setMessage(`无法读取年级列表：${error.message}`);
        setLoadState('error');
      });
  }, []);

  useEffect(() => {
    if (!grade) {
      setModules([]);
      setModuleName('');
      return;
    }

    setMessage('');
    fetchJson<string[]>('/api/modules', { grade })
      .then((items) => {
        setModules(items);
        setModuleName(items[0] ?? '');
        if (items.length === 0) {
          setMessage('当前年级暂无题目，请换一个年级，或先补充该年级的题目模板。');
        }
      })
      .catch((error: Error) => {
        setModules([]);
        setModuleName('');
        setMessage(`无法读取章节：${error.message}`);
      });
  }, [grade]);

  useEffect(() => {
    if (!grade || !moduleName) {
      setKnowledgePoints([]);
      setKnowledgePoint('');
      return;
    }

    setMessage('');
    fetchJson<KnowledgePoint[]>('/api/knowledge-points', { grade, module: moduleName })
      .then((items) => {
        setKnowledgePoints(items);
        setKnowledgePoint(items[0]?.name ?? '');
        if (items.length === 0) {
          setMessage('当前章节暂无题目，请换一个章节，或先补充该章节的题目模板。');
        }
      })
      .catch((error: Error) => {
        setKnowledgePoints([]);
        setKnowledgePoint('');
        setMessage(`无法读取知识点：${error.message}`);
      });
  }, [grade, moduleName]);

  useEffect(() => {
    if (viewMode === 'wrong-book') {
      void loadWrongBook();
    }
  }, [viewMode]);

  function resetAnswerState() {
    setAnswer('');
    setCheckResult(null);
    setShowSolution(false);
  }

  async function loadProblem(mode: 'knowledge' | 'random') {
    setLoadState('loading');
    setMessage('');
    resetAnswerState();

    try {
      const nextProblem =
        mode === 'knowledge' && canLoadByKnowledge
          ? await fetchJson<Problem>('/api/problem/by-knowledge', {
              grade,
              module: moduleName,
              knowledge_point: knowledgePoint,
            })
          : await fetchJson<Problem>(
              '/api/problem/random',
              grade ? { grade, ...(moduleName ? { module: moduleName } : {}) } : undefined,
            );

      setProblem(nextProblem);
      setLoadState('ready');
    } catch (error) {
      setProblem(null);
      setLoadState('error');
      setMessage(error instanceof Error ? `出题失败：${error.message}` : '出题失败');
    }
  }

  async function submitAnswer() {
    if (!problem || !answer.trim()) {
      setMessage('请先输入答案。');
      return;
    }

    setLoadState('loading');
    setMessage('');

    try {
      const result = await fetchJson<CheckResult>('/api/answer/check', undefined, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answer, problem_id: problem.problem_id }),
      });

      setCheckResult(result);
      setShowSolution(true);
      setLoadState('ready');
    } catch (error) {
      setLoadState('error');
      setMessage(error instanceof Error ? `判题失败：${error.message}` : '判题失败');
    }
  }

  async function loadWrongBook() {
    setWrongBookLoading(true);
    setWrongBookMessage('');

    try {
      const items = await fetchJson<WrongBookItem[]>('/api/wrong-book');
      setWrongBookItems(items);
    } catch (error) {
      setWrongBookItems([]);
      setWrongBookMessage(error instanceof Error ? `无法读取错题本：${error.message}` : '无法读取错题本');
    } finally {
      setWrongBookLoading(false);
    }
  }

  async function removeWrongBookItem(problemId: string) {
    setWrongBookLoading(true);
    setWrongBookMessage('');

    try {
      await fetchJson<{ removed: boolean; problem_id: string }>('/api/wrong-book/remove', undefined, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problem_id: problemId }),
      });
      await loadWrongBook();
    } catch (error) {
      setWrongBookMessage(error instanceof Error ? `移除错题失败：${error.message}` : '移除错题失败');
      setWrongBookLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-950">
      <div className="mx-auto flex min-h-screen w-full max-w-6xl flex-col gap-5 px-4 py-5 sm:px-6 lg:px-8">
        <header className="flex flex-col gap-3 border-b border-slate-200 pb-5 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-semibold text-cyan-700">MathPro</p>
            <h1 className="mt-1 text-2xl font-semibold tracking-normal text-slate-950 sm:text-3xl">
              数学刷题
            </h1>
          </div>
          <div className="flex flex-wrap gap-2 text-sm text-slate-600">
            <span className="rounded-md border border-slate-200 bg-white px-3 py-2">题库模板驱动</span>
            <span className="rounded-md border border-slate-200 bg-white px-3 py-2">默认端口 18080</span>
          </div>
        </header>

        <nav className="flex w-full gap-2 rounded-lg border border-slate-200 bg-white p-1 text-sm font-semibold">
          <button
            className={`flex-1 rounded-md px-4 py-2 transition ${
              viewMode === 'practice' ? 'bg-cyan-700 text-white' : 'text-slate-700 hover:bg-slate-50'
            }`}
            type="button"
            onClick={() => setViewMode('practice')}
          >
            刷题
          </button>
          <button
            className={`flex-1 rounded-md px-4 py-2 transition ${
              viewMode === 'wrong-book' ? 'bg-cyan-700 text-white' : 'text-slate-700 hover:bg-slate-50'
            }`}
            type="button"
            onClick={() => setViewMode('wrong-book')}
          >
            错题本
          </button>
        </nav>

        {viewMode === 'practice' ? (
        <section className="grid gap-4 lg:grid-cols-[320px_1fr]">
          <aside className="rounded-lg border border-slate-200 bg-white p-4">
            <h2 className="text-base font-semibold text-slate-900">练习范围</h2>

            <label className="mt-4 block text-sm font-medium text-slate-700" htmlFor="grade">
              年级
            </label>
            <select
              id="grade"
              className="mt-2 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100"
              value={grade}
              onChange={(event) => {
                setGrade(event.target.value);
                setProblem(null);
                resetAnswerState();
              }}
            >
              {grades.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>

            <label className="mt-4 block text-sm font-medium text-slate-700" htmlFor="module">
              章节
            </label>
            <select
              id="module"
              className="mt-2 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100"
              value={moduleName}
              onChange={(event) => {
                setModuleName(event.target.value);
                setProblem(null);
                resetAnswerState();
              }}
            >
              {modules.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>

            <label className="mt-4 block text-sm font-medium text-slate-700" htmlFor="knowledge-point">
              知识点
            </label>
            <select
              id="knowledge-point"
              className="mt-2 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100"
              value={knowledgePoint}
              onChange={(event) => {
                setKnowledgePoint(event.target.value);
                setProblem(null);
                resetAnswerState();
              }}
            >
              {knowledgePoints.map((item) => (
                <option key={item.id} value={item.name}>
                  {item.name}
                </option>
              ))}
            </select>

            <div className="mt-5 grid grid-cols-2 gap-3">
              <button
                className="rounded-md bg-cyan-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-cyan-800 disabled:cursor-not-allowed disabled:bg-slate-300"
                type="button"
                disabled={!canLoadByKnowledge || loadState === 'loading'}
                onClick={() => void loadProblem('knowledge')}
              >
                出题
              </button>
              <button
                className="rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-800 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:text-slate-400"
                type="button"
                disabled={!grade || loadState === 'loading'}
                onClick={() => void loadProblem('random')}
              >
                随机
              </button>
            </div>

            <div className="mt-5 rounded-md bg-slate-50 p-3 text-sm text-slate-600">
              <p>当前范围</p>
              <p className="mt-1 font-medium text-slate-900">
                {grade || '未选择'} / {moduleName || '未选择'} / {knowledgePoint || '未选择'}
              </p>
              {selectedPoint ? <p className="mt-1">学期：{selectedPoint.semester}</p> : null}
              {!hasPracticeScope && grade ? (
                <p className="mt-2 text-amber-700">当前年级暂无可练习题目。</p>
              ) : null}
            </div>
          </aside>

          <section className="rounded-lg border border-slate-200 bg-white p-4 sm:p-5">
            <div className="flex flex-col gap-3 border-b border-slate-200 pb-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-base font-semibold text-slate-900">题目</h2>
                {problem ? (
                  <p className="mt-1 text-sm text-slate-500">
                    {problem.grade} / {problem.module} / {problem.knowledge_point} / 难度 {problem.difficulty}
                  </p>
                ) : (
                  <p className="mt-1 text-sm text-slate-500">请选择范围后出题。</p>
                )}
              </div>
              {problem ? (
                <span className="w-fit rounded-md bg-slate-100 px-3 py-2 text-sm font-medium text-slate-700">
                  {problem.question_type}
                </span>
              ) : null}
            </div>

            {message ? (
              <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">
                {message}
              </div>
            ) : null}

            <div className="mt-5 min-h-40">
              {problem ? (
                <div>
                  <p className="text-sm text-slate-500">模板：{problem.template_id}</p>
                  <div className="mt-3 rounded-lg bg-slate-50 p-4 text-lg leading-8 text-slate-950">
                    <MathText text={problem.question} />
                  </div>

                  <label className="mt-5 block text-sm font-medium text-slate-700" htmlFor="answer">
                    你的答案
                  </label>
                  <div className="mt-2 flex flex-col gap-3 sm:flex-row">
                    <input
                      id="answer"
                      className="min-h-11 flex-1 rounded-md border border-slate-300 px-3 py-2 text-base outline-none focus:border-cyan-600 focus:ring-2 focus:ring-cyan-100"
                      value={answer}
                      onChange={(event) => setAnswer(event.target.value)}
                      onKeyDown={(event) => {
                        if (event.key === 'Enter') {
                          void submitAnswer();
                        }
                      }}
                      placeholder="输入答案，例如 A、3、x+1"
                    />
                    <button
                      className="rounded-md bg-slate-950 px-5 py-2 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
                      type="button"
                      disabled={loadState === 'loading'}
                      onClick={() => void submitAnswer()}
                    >
                      提交
                    </button>
                  </div>

                  {checkResult ? (
                    <div
                      className={`mt-4 rounded-md px-4 py-3 text-sm font-medium ${
                        checkResult.correct ? 'bg-emerald-50 text-emerald-800' : 'bg-rose-50 text-rose-800'
                      }`}
                    >
                      {checkResult.correct ? '回答正确' : '回答错误'}
                    </div>
                  ) : null}

                  {showSolution ? (
                    <div className="mt-4 rounded-lg border border-slate-200 p-4">
                      <h3 className="text-sm font-semibold text-slate-900">解析</h3>
                      <p className="mt-2 leading-8 text-slate-700">
                        <MathText text={problem.solution} />
                      </p>
                    </div>
                  ) : null}

                  <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:justify-end">
                    <button
                      className="rounded-md border border-slate-300 bg-white px-5 py-2 text-sm font-semibold text-slate-800 transition hover:bg-slate-50"
                      type="button"
                      onClick={() => {
                        setShowSolution((value) => !value);
                      }}
                    >
                      {showSolution ? '隐藏解析' : '查看解析'}
                    </button>
                    <button
                      className="rounded-md bg-cyan-700 px-5 py-2 text-sm font-semibold text-white transition hover:bg-cyan-800 disabled:cursor-not-allowed disabled:bg-slate-300"
                      type="button"
                      disabled={loadState === 'loading'}
                      onClick={() => void loadProblem(canLoadByKnowledge ? 'knowledge' : 'random')}
                    >
                      下一题
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex min-h-72 items-center justify-center rounded-lg bg-slate-50 p-6 text-center text-slate-600">
                  <p>选择年级、章节和知识点后点击“出题”，或直接在当前年级章节内随机练习。</p>
                </div>
              )}
            </div>
          </section>
        </section>
        ) : (
          <section className="rounded-lg border border-slate-200 bg-white p-4 sm:p-5">
            <div className="flex flex-col gap-3 border-b border-slate-200 pb-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-base font-semibold text-slate-900">错题本</h2>
                <p className="mt-1 text-sm text-slate-500">默认显示未移除的错题。</p>
              </div>
              <button
                className="rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-800 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:text-slate-400"
                type="button"
                disabled={wrongBookLoading}
                onClick={() => void loadWrongBook()}
              >
                刷新
              </button>
            </div>

            {wrongBookMessage ? (
              <div className="mt-4 rounded-md border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-900">
                {wrongBookMessage}
              </div>
            ) : null}

            <div className="mt-5">
              {wrongBookLoading && wrongBookItems.length === 0 ? (
                <div className="rounded-lg bg-slate-50 p-6 text-center text-sm text-slate-600">正在读取错题本...</div>
              ) : null}

              {!wrongBookLoading && wrongBookItems.length === 0 ? (
                <div className="rounded-lg bg-slate-50 p-6 text-center text-sm text-slate-600">暂无错题</div>
              ) : null}

              {wrongBookItems.length > 0 ? (
                <div className="grid gap-4">
                  {wrongBookItems.map((item) => (
                    <article key={item.id} className="rounded-lg border border-slate-200 p-4">
                      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                        <div>
                          <p className="text-sm font-semibold text-slate-900">
                            {item.grade} / {item.module} / {item.knowledge_point}
                          </p>
                          <p className="mt-1 text-sm text-slate-500">
                            {item.question_type} / 难度 {item.difficulty} / 错误 {item.wrong_count} 次
                          </p>
                        </div>
                        <button
                          className="w-fit rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-800 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:text-slate-400"
                          type="button"
                          disabled={wrongBookLoading}
                          onClick={() => void removeWrongBookItem(item.problem_id)}
                        >
                          移除错题
                        </button>
                      </div>

                      <div className="mt-4 rounded-lg bg-slate-50 p-4 text-base leading-8 text-slate-950">
                        <MathText text={item.question} />
                      </div>

                      <div className="mt-4 grid gap-3 md:grid-cols-[220px_1fr]">
                        <div className="rounded-md bg-rose-50 p-3 text-sm text-rose-800">
                          <p className="font-semibold">我的最后错误答案</p>
                          <p className="mt-1 break-words">{item.last_wrong_answer}</p>
                        </div>
                        <div className="rounded-md border border-slate-200 p-3 text-sm text-slate-700">
                          <p className="font-semibold text-slate-900">解析</p>
                          <p className="mt-2 leading-8">
                            <MathText text={item.solution} />
                          </p>
                        </div>
                      </div>
                    </article>
                  ))}
                </div>
              ) : null}
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
