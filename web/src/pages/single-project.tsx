import { useEffect, useState } from "react";
import { HiArrowLeft } from "react-icons/hi";
import { Link, useParams } from "react-router-dom";
import PageHeader from "../components/page-header";
import TaskList from "../components/task-list";
import ProjectService from "../services/projects";
import TaskService, { Task } from "../services/tasks";

type Project = {
  id: number;
  title: string;
  description?: string;
  created_at: string;
};

const SingleProjectPage = () => {
  const { projectId } = useParams();
  const [project, setProject] = useState<Project | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      ProjectService.getById(parseInt(projectId as string)),
      TaskService.getAll(parseInt(projectId as string)),
    ])
      .then((values) => {
        setProject(values[0]);
        setTasks(values[1]);
      })
      .catch((error) => setError(error));
  }, []);

  return (
    <div className="flex flex-col">
      <PageHeader>
        <div className="flex gap-4">
          <Link to="/projects">
            <span className="p-3 font-bold inline-flex text-grey-dark ring-1 ring-slate-900/10 rounded-lg hover:text-primary hover:bg-grey-lightest hover:ring-primary">
              <HiArrowLeft />
            </span>
          </Link>
          <h1 className="font-bold text-3xl text-grey-dark ml-4">
            {project?.title}
          </h1>
        </div>
        <div className="toolbar">Toolbar</div>
      </PageHeader>
      <section>
        <TaskList tasks={tasks} />
      </section>
    </div>
  );
};

export default SingleProjectPage;
