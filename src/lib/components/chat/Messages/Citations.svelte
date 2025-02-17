<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import Collapsible from '$lib/components/common/Collapsible.svelte';
	import ChevronDown from '$lib/components/icons/ChevronDown.svelte';
	import ChevronUp from '$lib/components/icons/ChevronUp.svelte';
	import { showPdfViewer } from '$lib/stores';

	import PdfViewer from '$lib/components/chat/Messages/Pdf/PdfViewer.svelte'; // Import PdfViewer component

	const i18n = getContext('i18n');

	export let sources = [];

	let citations = [];
	let showPercentage = false;
	let showRelevance = true;

	let selectedCitation: any = null;
	let isCollapsibleOpen = false;

	//export let isPdfExpanded = false; // New prop to control expansion
	//let showPdfViewer = false; // Flag to control PDF visibility

	//function togglePdfExpansion() {
	//	showPdfViewer = !showPdfViewer; // Toggle the expansion state
	//}

	// Function to handle the visibility of the PDF viewer when a citation is clicked
	async function togglePdfViewerVisibility(citation: any) {
		// Check if the citation is already selected
		if (selectedCitation && selectedCitation.id === citation.id) {
			// If the same citation is clicked, toggle visibility
			showPdfViewer.update(value => !value);
		} else {
			// Otherwise, select the new citation and show the PDF
			selectedCitation = citation;
			showPdfViewer.update(value => true);
			await fetchCitationPDF(citation);
		}
	}

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
		// Automatically select the first citation
		if (citations.length > 0 && !selectedCitation) {
			const firstCitation = citations[0];
			selectedCitation = firstCitation;

			// Fetch the PDF path for the first citation
			fetchCitationPDF(firstCitation);
		}
	});

	async function fetchCitationPDF(citation: any) {
		try {
			const response = await fetch(citation.source.url);
			if (response.ok) {
				const data = await response.json();
				if (data.path?.endsWith('.pdf')) {
					const decodedPath = decodeURIComponent(data.path);
					const fileName = decodedPath.split('/').pop(); // Extract filename from path
					selectedCitation = { ...citation, pdfPath: fileName };
				}
			} else {
				console.error('Failed to fetch citation data:', response.status);
			}
		} catch (error) {
			console.error('Error fetching citation path:', error);
		}
	}
</script>

<!-- Main Citation List -->
{#if citations.length > 0}
	<div class="py-0.5 -mx-0.5 w-full flex gap-1 items-center flex-wrap">
		{#each citations as citation, idx}
			<button
				id={`source-${citation.source.name}`}
				class="no-toggle outline-none flex dark:text-gray-300 p-1 bg-white dark:bg-gray-900 rounded-xl max-w-96"
				on:click={() => togglePdfViewerVisibility(citation)}
			>
				{#if citations.every((c) => c.distances !== undefined)}
					<div class="bg-gray-50 dark:bg-gray-800 rounded-full size-4">{idx + 1}</div>
				{/if}
				<div
					class="flex-1 mx-1 line-clamp-1 text-black/60 hover:text-black dark:text-white/60 dark:hover:text-white transition"
				>
					{citation.source.name}
				</div>
			</button>
		{/each}
	</div>
{/if}

<!-- Conditionally Render PDF Viewer -->
{#if showPdfViewer && selectedCitation?.pdfPath}
	<PdfViewer selectedCitation={selectedCitation} />
{/if}
