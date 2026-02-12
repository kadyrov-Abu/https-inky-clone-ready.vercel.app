npm create vite@latest inky-clone-vercel
cd inky-clone-vercel
npm install react react-dom react-scripts react-beautiful-dnd
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  background-color: #f7f7f7;
}
import { useState, useEffect } from "react";
import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";

export default function App() {
  const [blocks, setBlocks] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [templateName, setTemplateName] = useState("");

  useEffect(() => {
    const savedBlocks = localStorage.getItem("inkyBlocks");
    const savedTemplates = localStorage.getItem("inkyTemplates");
    if (savedBlocks) setBlocks(JSON.parse(savedBlocks));
    if (savedTemplates) setTemplates(JSON.parse(savedTemplates));
  }, []);

  useEffect(() => {
    localStorage.setItem("inkyBlocks", JSON.stringify(blocks));
  }, [blocks]);

  useEffect(() => {
    localStorage.setItem("inkyTemplates", JSON.stringify(templates));
  }, [templates]);

  const addBlock = (type) => {
    setBlocks([...blocks, { id: Date.now().toString(), type, content: "", style: {} }]);
  };

  const updateBlock = (id, key, value) => {
    setBlocks(blocks.map(b => b.id === id ? { ...b, [key]: value } : b));
  };

  const exportHTML = () => {
    const html = blocks.map(b => {
      const style = Object.entries(b.style || {}).map(([k,v]) => `${k}:${v}`).join(";");
      if (b.type === "header") return `<h1 style="${style}">${b.content}</h1>`;
      if (b.type === "paragraph") return `<p style="${style}">${b.content}</p>`;
      if (b.type === "button") return `<button style="${style}">${b.content}</button>`;
      if (b.type === "image") return `<img src="${b.content}" alt="" style="${style}"/>`;
    }).join("\n");
    navigator.clipboard.writeText(html);
    alert("HTML скопирован в буфер!");
  };

  const saveTemplate = () => {
    if (!templateName) return alert("Введите имя шаблона!");
    setTemplates([...templates, { name: templateName, blocks }]);
    setTemplateName("");
  };

  const loadTemplate = (template) => {
    setBlocks(template.blocks);
  };

  const onDragEnd = (result) => {
    if (!result.destination) return;
    const reordered = Array.from(blocks);
    const [moved] = reordered.splice(result.source.index, 1);
    reordered.splice(result.destination.index, 0, moved);
    setBlocks(reordered);
  };

  const generatePreviewHTML = () => {
    return `
      <html>
        <body>${blocks.map(b => {
          const style = Object.entries(b.style || {}).map(([k,v]) => `${k}:${v}`).join(";");
          if (b.type === "header") return `<h1 style="${style}">${b.content}</h1>`;
          if (b.type === "paragraph") return `<p style="${style}">${b.content}</p>`;
          if (b.type === "button") return `<button style="${style}">${b.content}</button>`;
          if (b.type === "image") return `<img src="${b.content}" alt="" style="${style}"/>`;
        }).join("")}</body>
      </html>
    `;
  };

  return (
    <div className="p-6 max-w-7xl mx-auto flex gap-6">
      {/* Меню */}
      <div className="w-1/3 space-y-4">
        <h1 className="text-2xl font-bold mb-4">Check Inky Clone</h1>
        <div className="space-x-2 mb-4 flex flex-wrap gap-2">
          <button onClick={() => addBlock("header")} className="bg-blue-500 text-white px-4 py-2 rounded">Добавить Заголовок</button>
          <button onClick={() => addBlock("paragraph")} className="bg-green-500 text-white px-4 py-2 rounded">Добавить Параграф</button>
          <button onClick={() => addBlock("button")} className="bg-yellow-500 text-white px-4 py-2 rounded">Добавить Кнопку</button>
          <button onClick={() => addBlock("image")} className="bg-purple-500 text-white px-4 py-2 rounded">Добавить Картинку</button>
          <button onClick={exportHTML} className="bg-red-500 text-white px-4 py-2 rounded">Экспорт HTML</button>
        </div>

        {/* Drag & Drop */}
        <DragDropContext onDragEnd={onDragEnd}>
          <Droppable droppableId="blocks">
            {(provided) => (
              <div {...provided.droppableProps} ref={provided.innerRef} className="space-y-4">
                {blocks.map((block, index) => (
                  <Draggable key={block.id} draggableId={block.id} index={index}>
                    {(provided) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        className="border p-2 rounded bg-gray-50"
                      >
                        {block.type === "image" ? (
                          <input
                            type="text"
                            placeholder="Ссылка на изображение"
                            value={block.content}
                            onChange={(e) => updateBlock(block.id, "content", e.target.value)}
                            className="border p-2 w-full mb-2"
                          />
                        ) : (
                          <textarea
                            placeholder={`Введите текст для ${block.type}`}
                            value={block.content}
                            onChange={(e) => updateBlock(block.id, "content", e.target.value)}
                            className="border p-2 w-full mb-2"
                          />
                        )}

                        <div className="flex gap-2 mb-2">
                          <input
                            type="color"
                            value={block.style.color || "#000000"}
                            onChange={(e) => updateBlock(block.id, "style", { ...block.style, color: e.target.value })}
                          />
                          <input
                            type="color"
                            value={block.style.backgroundColor || "#ffffff"}
                            onChange={(e) => updateBlock(block.id, "style", { ...block.style, backgroundColor: e.target.value })}
                          />
                        </div>
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>

        {/* Шаблоны */}
        <div className="mt-4 space-y-2">
          <input
            type="text"
            placeholder="Имя шаблона"
            value={templateName}
            onChange={(e) => setTemplateName(e.target.value)}
            className="border p-2 w-full"
          />
          <button onClick={saveTemplate} className="bg-indigo-500 text-white px-4 py-2 rounded w-full">Сохранить шаблон</button>

          {templates.map((t,i) => (
            <button
              key={i}
              onClick={() => loadTemplate(t)}
              className="block w-full text-left border p-2 rounded mb-1 bg-gray-100 hover:bg-gray-200"
            >
              {t.name}
            </button>
          ))}
        </div>
      </div>

      {/* Превью */}
      <div className="w-2/3 border p-4 rounded bg-white h-[80vh] overflow-auto">
        <h2 className="text-xl font-semibold mb-4">Preview</h2>
        <iframe
          title="preview"
          srcDoc={generatePreviewHTML()}
          className="w-full h-full border"
        />
      </div>
    </div>
  );
}
