
#!/bin/sh



conda () {
	if [ "$#" -lt 1 ]
	then
		$_CONDA_EXE
	else
		\local cmd="$1"
		shift
		case "$cmd" in
			(activate) _conda_activate "$@" ;;
			(deactivate) _conda_deactivate "$@" ;;
			(install | update | uninstall | remove) $_CONDA_EXE "$cmd" "$@" && _conda_reactivate ;;
			(*) $_CONDA_EXE "$cmd" "$@" ;;
		esac
	fi
}
