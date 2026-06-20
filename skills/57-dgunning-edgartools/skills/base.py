"""
Base class for EdgarTools AI skills.

Provides the foundation for creating AI skills that integrate with
edgar.ai infrastructure. External packages can subclass BaseSkill to
create specialized skills (e.g., insider trading detection, fraud analysis).
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Dict, List, Optional

__all__ = ['BaseSkill']


class BaseSkill(ABC):
    """
    Abstract base class for EdgarTools AI skills.

    A skill packages:
    - Documentation (markdown files with YAML frontmatter)
    - Helper functions (workflow wrappers)
    - Examples and patterns

    External packages can subclass this to create specialized skills
    that integrate seamlessly with edgar.ai infrastructure.

    Example:
        >>> from edgar.ai.skills.base import BaseSkill
        >>> from pathlib import Path
        >>>
        >>> class InsiderTradingSkill(BaseSkill):
        ...     @property
        ...     def name(self) -> str:
        ...         return "Insider Trading Detection"
        ...
        ...     @property
        ...     def description(self) -> str:
        ...         return "Analyze Form 4 filings for insider trading patterns"
        ...
        ...     @property
        ...     def content_dir(self) -> Path:
        ...         return Path(__file__).parent / "content"
        ...
        ...     def get_helpers(self) -> Dict[str, Callable]:
        ...         return {
        ...             'detect_unusual_trades': self.detect_unusual_trades,
        ...         }
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Skill name for display and identification.

        Should be descriptive and unique. Example: "SEC Filing Analysis"

        Returns:
            Human-readable skill name
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Brief description of skill capabilities.

        Used by AI agents to determine when to activate the skill.
        Should clearly describe what problems the skill solves.

        Returns:
            One-sentence skill description
        """
        pass

    @property
    @abstractmethod
    def content_dir(self) -> Path:
        """
        Directory containing skill documentation (markdown files).

        This directory should contain:
        - skill.md: Main skill documentation with YAML frontmatter
        - objects.md: Object reference (optional)
        - workflows.md: Workflow patterns (optional)
        - readme.md: Installation/overview (optional)

        Returns:
            Path to skill content directory
        """
        pass

    @abstractmethod
    def get_helpers(self) -> Dict[str, Callable]:
        """
        Return dictionary of helper functions this skill provides.

        Helper functions are convenience wrappers that simplify
        common workflows for the skill's domain.

        Returns:
            Dict mapping function names to callable objects

        Example:
            >>> {
            ...     'get_revenue_trend': helpers.get_revenue_trend,
            ...     'compare_companies': helpers.compare_companies,
            ... }
        """
        pass

    # Non-abstract methods with default implementations

    def get_object_docs(self) -> List[Path]:
        """
        Return paths to centralized object documentation files to include in exports.

        Override this method to specify which centralized API reference docs
        should be included when exporting the skill. These docs are copied to
        an 'api-reference/' subdirectory in the exported skill package.

        Returns:
            List of Path objects pointing to markdown documentation files

        Example:
            >>> def get_object_docs(self) -> List[Path]:
            ...     from pathlib import Path
            ...     root = Path(__file__).parent.parent.parent
            ...     return [
            ...         root / "entity/docs/Company.md",
            ...         root / "xbrl/docs/XBRL.md",
            ...     ]
        """
        return []  # Default: no object docs

    def get_documents(self) -> List[str]:
        """
        List of markdown documents in this skill.

        Returns:
            List of document names (without .md extension)
        """
        if not self.content_dir.exists():
            return []
        return [f.stem for f in self.content_dir.glob("*.md")]

    def get_document_content(self, name: str) -> str:
        """
        Get content of a specific markdown document.

        Args:
            name: Document name (with or without .md extension)

        Returns:
            Full markdown content as string

        Raises:
            FileNotFoundError: If document doesn't exist
        """
        doc_name = name if name.endswith('.md') else f"{name}.md"
        doc_path = self.content_dir / doc_name

        if not doc_path.exists():
            available = ", ".join(self.get_documents())
            raise FileNotFoundError(
                f"Document '{name}' not found in skill '{self.name}'. "
                f"Available: {available}"
            )

        return doc_path.read_text()

    def export(self, format: str = "claude-desktop", output_dir: Optional[Path] = None, **kwargs) -> Path:
        """
        Export skill in specified format.

        Args:
            format: Export format (default: "claude-desktop")
                - "claude-desktop": Claude Desktop Skills format (ZIP)
                - "claude-skills": Official Claude Skills format (~/.claude/skills/)
            output_dir: Where to create export (default: ./skills_export/)
            **kwargs: Additional format-specific parameters
                - create_zip (bool): For claude-desktop format (default: True)
                - install (bool): For claude-skills format (default: True)

        Returns:
            Path to exported skill directory or archive

        Example:
            >>> skill = EdgarToolsSkill()
            >>> # Export as ZIP for Claude Desktop upload
            >>> path = skill.export(format="claude-desktop")
            >>> # Export to ~/.claude/skills/ for automatic discovery
            >>> path = skill.export(format="claude-skills")
        """
        from edgar.ai.exporters import export_skill
        return export_skill(self, format=format, output_dir=output_dir, **kwargs)

    def __repr__(self) -> str:
        """String representation of the skill."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __str__(self) -> str:
        """Human-readable skill description."""
        docs_count = len(self.get_documents())
        helpers_count = len(self.get_helpers())
        return (
            f"Skill: {self.name}\n"
            f"Description: {self.description}\n"
            f"Documents: {docs_count}\n"
            f"Helper Functions: {helpers_count}"
        )
