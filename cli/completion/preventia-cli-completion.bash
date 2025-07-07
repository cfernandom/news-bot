
# Bash completion for preventia-cli
_preventia_cli_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Main commands
    if [ $COMP_CWORD -eq 1 ]; then
        opts="scraper source user compliance status serve backup version docs"
        COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
        return 0
    fi

    # Subcommands
    case "${COMP_WORDS[1]}" in
        scraper)
            opts="list run run-all status validate"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        source)
            opts="list show create update delete validate"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        user)
            opts="list show create update reset-password assign-role revoke-role list-roles"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
        compliance)
            opts="dashboard violations validate-all audit create-notice notices"
            COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
            ;;
    esac
}

complete -F _preventia_cli_completion preventia-cli
