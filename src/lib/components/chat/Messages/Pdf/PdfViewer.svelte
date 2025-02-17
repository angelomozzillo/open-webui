<script lang="ts">
	import { showPdfViewer } from '$lib/stores';
	import ChevronLeft from '$lib/components/icons/ChevronLeft.svelte';

	export let selectedCitation; // Now we receive this as a prop

	function togglePdf() {
		showPdfViewer.update((v) => !v);
		console.log('Toggled PDF, new value:', $showPdfViewer); // Debugging log
	}
</script>

<div
	class="relative flex transition-[width] duration-300 ease-in-out"
	style="width: {$showPdfViewer ? '40%' : '0'};"
>
	<!-- PDF Viewer -->
	<div
		class="h-full w-full border rounded-xl overflow-hidden shadow-lg bg-white transition-[opacity,width] duration-300 ease-in-out"
		style="width: {$showPdfViewer ? '100%' : '0'}; opacity: {$showPdfViewer
			? '1'
			: '0'}; position: relative; top: -20px;"
	>
		{#if $showPdfViewer}
			<iframe
				src={`/uploads/${selectedCitation?.pdfPath}#zoom=100`}
				type="application/pdf"
				class="w-full h-full"
			></iframe>
		{/if}
	</div>

	<!-- Toggle Button (Now Independent) -->
	<button
		class="absolute top-1/2 transform -translate-y-1/2 z-50 bg-gray-800 text-white p-2 rounded-l-lg shadow-md transition-all duration-300 ease-in-out"
		on:click={togglePdf}
		style="left: {$showPdfViewer ? '-20px' : '-40px'};"
	>
		{#if $showPdfViewer}
			<ChevronRight />
		{:else}
			<ChevronLeft />
		{/if}
	</button>
</div>
