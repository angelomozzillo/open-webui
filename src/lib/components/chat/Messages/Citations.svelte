<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import Collapsible from '$lib/components/common/Collapsible.svelte';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import ChevronUp from '$lib/components/icons/ChevronUp.svelte';

	const i18n = getContext('i18n');

	export let sources = [];

	let citations = [];
	let showPercentage = false;
	let showRelevance = true;

	let selectedCitation: any = null;
	let isCollapsibleOpen = false;

	function calculateShowRelevance(sources: any[]) {
		const distances = sources.flatMap((citation) => citation.distances ?? []);
		const inRange = distances.filter((d) => d !== undefined && d >= -1 && d <= 1).length;
		const outOfRange = distances.filter((d) => d !== undefined && (d < -1 || d > 1)).length;

		if (distances.length === 0) {
			return false;
		}

		if (
			(inRange === distances.length - 1 && outOfRange === 1) ||
			(outOfRange === distances.length - 1 && inRange === 1)
		) {
			return false;
		}

		return true;
	}

	function shouldShowPercentage(sources: any[]) {
		const distances = sources.flatMap((citation) => citation.distances ?? []);
		return distances.every((d) => d !== undefined && d >= -1 && d <= 1);
	}

	$: {
		citations = sources.reduce((acc, source) => {
			if (Object.keys(source).length === 0) {
				return acc;
			}

			source.document.forEach((document, index) => {
				const metadata = source.metadata?.[index];
				const distance = source.distances?.[index];

				const id = metadata?.source ?? 'N/A';
				let _source = source?.source;

				if (metadata?.name) {
					_source = { ..._source, name: metadata.name };
				}

				if (id.startsWith('http://') || id.startsWith('https://')) {
					_source = { ..._source, name: id, url: id };
				}

				const existingSource = acc.find((item) => item.id === id);

				if (existingSource) {
					existingSource.document.push(document);
					existingSource.metadata.push(metadata);
					if (distance !== undefined) existingSource.distances.push(distance);
				} else {
					acc.push({
						id: id,
						source: _source,
						document: [document],
						metadata: metadata ? [metadata] : [],
						distances: distance !== undefined ? [distance] : undefined
					});
				}
			});
			return acc;
		}, []);

		showRelevance = calculateShowRelevance(citations);
		showPercentage = shouldShowPercentage(citations);
	}

	onMount(() => {
		console.log('onMount triggered');
    	if (citations.length > 0) {
			selectedCitation = citations.find(citation => citation.source.url?.endsWith('.pdf')) || citations[0];
			if (selectedCitation?.source?.url?.endsWith('.pdf')) {
				console.log('PDF Source:', selectedCitation.source.url);
			} else {
				console.log(selectedCitation.source.url);
			}
    	}
	});
</script>

<style>
	.sidebar {
		@apply fixed top-0 right-0 w-80 h-full bg-white dark:bg-gray-900 shadow-xl transform transition-transform duration-300 ease-in-out;
		transform: translateX(100%);
	}
	.sidebar.open {
		transform: translateX(0);
	}
	.pdf-viewer {
		@apply w-full h-full;
		border: none;
	}
</style>

<!-- Main Citation List -->
{#if citations.length > 0}
	<div class="py-0.5 -mx-0.5 w-full flex gap-1 items-center flex-wrap">
		{#each citations as citation, idx}
			<button
				id={`source-${citation.source.name}`}
				class="no-toggle outline-none flex dark:text-gray-300 p-1 bg-white dark:bg-gray-900 rounded-xl max-w-96"
				on:click={() => (selectedCitation = citation)}
			>
				{#if citations.every((c) => c.distances !== undefined)}
					<div class="bg-gray-50 dark:bg-gray-800 rounded-full size-4">{idx + 1}</div>
				{/if}
				<div class="flex-1 mx-1 line-clamp-1 text-black/60 hover:text-black dark:text-white/60 dark:hover:text-white transition">
					{citation.source.name}
				</div>
			</button>
		{/each}
	</div>
{/if}

<!-- Sidebar Panel for Citation Details -->
<div class={`sidebar ${selectedCitation ? 'open' : ''}`}>
	{#if selectedCitation}
		<div class="p-4 flex flex-col h-full">
			<button class="self-end text-gray-500 hover:text-gray-800" on:click={() => (selectedCitation = null)}>
				&times;
			</button>
			<h2 class="text-lg font-bold mb-2">{selectedCitation.source.name}</h2>

			<div class="overflow-y-auto flex-1">
				{#if selectedCitation.source.url && selectedCitation.source.url.endsWith('.pdf')}
					<!-- PDF Viewer -->
					<iframe src={selectedCitation.source.url} class="pdf-viewer"></iframe>
				{:else}
					<!-- Fallback for Text Documents -->
					{#each selectedCitation.document as doc}
						<p class="mb-2 text-sm text-gray-700 dark:text-gray-300">{doc}</p>
					{/each}
				{/if}
			</div>
		</div>
	{/if}
</div>
