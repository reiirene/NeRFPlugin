# Unity 自动导入系统说明文档

## 📌 简介

本项目包含两部分核心功能脚本：

1. **AutoObjToPrefab.cs**  
   用于监听项目中 `Assets/Resources/Models/` 文件夹下新增的 `.obj` 或 `.ply` 文件，自动将其转换为 `.prefab` 并实例化进当前场景。

2. **PlyImporter.cs**  
   用于解析 `.ply` 格式的 ASCII 点云文件并构建为 Unity `Mesh`。支持基础的顶点与三角面数据的构建。

---

## 🧩 使用方式

### 项目结构要求

请确保你的 `.obj` 或 `.ply` 文件位于以下路径：

```
Assets/
└── Resources/
    └── Models/
        ├── cube.obj
        ├── sample.ply
```

### 自动处理流程

1. 将 `.obj` 或 `.ply` 拖入 `Assets/Resources/Models/` 文件夹。
2. Unity 会自动触发 `AssetPostprocessor`：
   - 生成对应 `.prefab`（如 `cube.prefab`）
   - 并自动将其实例化至当前场景（默认位置为 `Vector3.zero`）
3. 控制台会显示模型导入与处理的日志信息。

---

## 🔍 功能说明

### AutoObjToPrefab.cs

- 类型：`AssetPostprocessor`
- 作用：检测新导入的 `.obj` / `.ply`，生成 prefab 并实例化。
- 支持：
  - `.obj` 模型（Unity 原生支持）
  - `.ply` 模型（需配合 `PlyImporter` 使用）

### PlyImporter.cs

- 类型：`静态工具类`
- 功能：将 `.ply` ASCII 文件内容解析为 `Mesh` 对象
- 支持：
  - `element vertex N`
  - `element face N`
  - 顶点：`x y z` 格式，空格分隔
  - 面：目前支持三角面（3 x y z）

---

## ⚠️ 使用限制与注意事项

| 类型 | 限制说明 |
|------|----------|
| `.ply` 格式 | 仅支持 ASCII 格式的 `.ply`，不支持 binary 编码版本 |
| `.ply` 内容 | 需明确包含 `end_header`，顶点与面必须完整，暂不支持颜色、法线、纹理等附加属性 |
| 错误处理 | 若 `.ply` 文件结构异常（如行空、格式不规范等），控制台将抛出错误但不会中断其他模型处理 |
| 重复实例化 | 同名 prefab 会被覆盖，新导入模型会重复实例化；建议运行完毕后清理旧实例 |
| 执行环境 | 需使用 Unity 编辑器运行，无法在打包后的客户端中动态加载 |

---

## 🧪 示例日志（Console 输出）

```
🛠 检测到新 .obj 模型: Assets/Resources/Models/cube.obj
✅ 已自动生成 prefab: Assets/Resources/Models/cube.prefab
🟢 模型已自动加载到场景: cube

🛠 检测到新 .ply 模型: Assets/Resources/Models/cone.ply
✅ 已自动生成 prefab: Assets/Resources/Models/cone.prefab
🟢 模型已自动加载到场景: cone
```

---

## 📁 文件位置
Assets/
└──Docs/
    └──README_AutoImporter.md
├──Editor/
    └──AutoObjToPrefab.cs
├──Resources/
├──Scripts/
    └──PlyImporter.cs

